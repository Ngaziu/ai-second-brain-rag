import os
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
import textwrap

# --- CONFIGURAZIONE ---
db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"

def get_retrieved_context(query, n_results=3):
    """Cerca nel database vettoriale locale i frammenti più rilevanti."""
    print("Cerco nel tuo disco fisso (ChromaDB locale)...")
    client = chromadb.PersistentClient(path=db_dir)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    collection = client.get_collection(name="second_brain_collection", embedding_function=emb_fn)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    context = ""
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        source = results['metadatas'][0][i]['source']
        context += f"\n--- Fonte: {source} ---\n{doc}\n"
        
    return context

def generate_rag_answer(query, context):
    """Chiama il modello Gemini tramite API per formulare la risposta."""
    prompt = f"""Sei l'assistente personale (Second Brain) di Schip.
Il tuo compito è rispondere alla domanda dell'utente basandoti ESCLUSIVAMENTE sulle informazioni del contesto fornito qui sotto, che deriva dai suoi corsi (video e slide).

REGOLE (Dal file AGENTS.md):
- Non inventare nulla (no allucinazioni). Se la risposta non c'è nel contesto, di' "Non ho trovato questa informazione nei tuoi corsi".
- Usa un linguaggio semplice, niente termini tecnici senza definirli, frasi corte.
- Cita sempre la fonte (es. "Come spiegato nel video X...").

CONTESTO RECUPERATO DAI CORSI:
{context}

DOMANDA DELL'UTENTE: {query}
"""
    # Usiamo il modello veloce e potente per i testi
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def main():
    print("\n" + "="*50)
    print(" BENVENUTO NEL TUO SECOND BRAIN (Powered by Gemini) ")
    print("="*50 + "\n")
    
    # Chiediamo la chiave API al primo avvio
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Non hai bisogno di LM Studio! Basta la tua chiave di Google AI Studio.")
        api_key = input("Incolla qui la tua API Key di Gemini e premi Invio:\n> ").strip()
        os.environ["GEMINI_API_KEY"] = api_key
    
    genai.configure(api_key=api_key)
    
    while True:
        query = input("\nFai una domanda ai tuoi corsi (o scrivi 'esci'):\n> ")
        if query.lower() in ['esci', 'exit', 'quit']:
            break
            
        # 1. Recupero informazioni in LOCALE (massima privacy per i tuoi dati)
        context = get_retrieved_context(query)
        
        print("\n" + "-"*30)
        print("CONTESTO TROVATO NEL TUO PC (I 3 frammenti migliori):")
        print(textwrap.shorten(context, width=500, placeholder="... [testo troncato per leggibilita']"))
        print("-"*30 + "\n")
        
        # 2. Generazione risposta in CLOUD (inviamo solo i 3 frammentini a Gemini)
        print("Spedisco i frammenti a Gemini per formulare la risposta...")
        try:
            answer = generate_rag_answer(query, context)
            print("\nRISPOSTA DEL SECOND BRAIN:\n")
            print(answer)
        except Exception as e:
            print(f"\n[ERRORE API GEMINI]: Assicurati che la chiave sia corretta. Dettaglio: {e}")
            
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
