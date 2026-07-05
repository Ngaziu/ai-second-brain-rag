import os
import time
import re
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from flask import Flask, render_template, request, jsonify
import math
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

# Percorso relativo: cerca la cartella chroma_db nella stessa posizione di questo file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(BASE_DIR, "chroma_db")

# Caricamento Cache Globale dei Metadati all'avvio
print("Inizializzazione Cache dei Nomi File da ChromaDB...")
ALL_SOURCES = set()
try:
    _client = chromadb.PersistentClient(path=db_dir)
    _collection = _client.get_collection(name="second_brain_collection")
    _total_docs = _collection.count()
    if _total_docs > 0:
        _batch_size = 500
        _batches = math.ceil(_total_docs / _batch_size)
        for i in range(_batches):
            _docs = _collection.get(limit=_batch_size, offset=i*_batch_size, include=["metadatas"])
            for m in _docs["metadatas"]:
                if m and "source" in m:
                    ALL_SOURCES.add(m["source"])
    print(f"Cache caricata: {len(ALL_SOURCES)} file unici pronti per il Fuzzy Matching.")
except Exception as e:
    print(f"Attenzione: Impossibile precaricare la cache dei file ({e})")


def get_retrieved_context(query, n_results=10, file_filter=None):
    client = chromadb.PersistentClient(path=db_dir)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    collection = client.get_collection(name="second_brain_collection", embedding_function=emb_fn)
    
    where_clause = None
    if file_filter:
        print(f"Applico filtro fuzzy per: '{file_filter}'")
        # Pulisci il filtro e dividi in parole chiave
        keywords = file_filter.lower().replace("'", "").replace('"', '').split()
        
        matched_sources = []
        for s in ALL_SOURCES:
            # Normalizziamo il nome del file (sostituiamo underscore e trattini con spazi)
            s_lower = s.lower().replace("_", " ").replace("-", " ")
            # Se tutte le parole chiave estratte sono nel nome del file, è un match
            if all(kw in s_lower for kw in keywords):
                matched_sources.append(s)
        
        if matched_sources:
            print(f"Fuzzy Match trovato! {len(matched_sources)} file corrispondenti.")
            if len(matched_sources) == 1:
                where_clause = {"source": {"$eq": matched_sources[0]}}
            else:
                # Limitiamo a 50 per evitare errori "too many SQL variables"
                where_clause = {"$or": [{"source": {"$eq": m}} for m in matched_sources[:50]]}
        else:
            print("Nessun Fuzzy Match trovato. Rimuovo il filtro per fallback.")
            where_clause = None
        
    if where_clause:
        results = collection.query(query_texts=[query], n_results=n_results, where=where_clause)
    else:
        results = collection.query(query_texts=[query], n_results=n_results)
    
    context = ""
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        # source = results['metadatas'][0][i]['source'] # Rimossa la citazione del file per anonimato
        context += f"\n--- Frammento di Conoscenza ---\n{doc}\n"
        
    return context

def extract_file_filter(query):
    prompt = f"""Analizza la seguente domanda dell'utente e capisci se sta chiedendo di cercare informazioni all'interno di uno SPECIFICO file, corso o cartella.
Se sì, estrai SOLO le parole chiave più significative che potrebbero comporre il nome del file (es. se dice 'dal pdf Talent Garden', rispondi 'Talent_Garden' o 'Talent Garden').
Se non sta specificando una fonte precisa ma fa una domanda generale, rispondi ESATTAMENTE con la parola "NESSUNO".
Non aggiungere punteggiatura, non scrivere frasi complete. Solo le parole chiave o NESSUNO.

Domanda: {query}"""
    
    # La scansione ha rivelato che i modelli 1.5 e 2.0 sono deprecati o bloccati sul free tier.
    # Usiamo l'alias stabile universale che Google aggiorna automaticamente all'ultimo Flash gratuito.
    available_model = 'gemini-2.5-flash'
                
    model = genai.GenerativeModel(available_model)
    
    # Facciamo un solo tentativo per il filtro. Se fallisce per 429, avvisiamo subito.
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        if result.upper() == "NESSUNO" or result == "":
            return None
        return result
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "quota" in error_str:
            raise Exception("Hai superato il limite gratuito di Gemini (circa 15 richieste al minuto). Attendi circa 60 secondi e riprova!")
        raise

def generate_rag_answer(query, context):
    prompt = f"""Sei il Second Brain ufficiale e l'assistente AI di Domenico Schipani.
Il tuo compito è rispondere alla domanda dell'utente basandoti ESCLUSIVAMENTE sulle informazioni del contesto fornito qui sotto.
Questo contesto rappresenta il know-how e il metodo di lavoro consolidato da Domenico Schipani.

REGOLE CRITICHE DI ANONIMIZZAZIONE E BRANDING:
1. NON nominare MAI autori, formatori esterni, nomi di corsi o brand (es. Raffaele Gaito, Learnn, Talent Garden, ecc.) anche se appaiono nel contesto.
2. Fai finta che tutte le informazioni fornite siano state scritte, create o teorizzate direttamente da Domenico Schipani.
3. Usa frasi come "Secondo il mio metodo...", "Come consiglio spesso...", "Nella mia esperienza di Digital Strategist...".
4. Se l'utente chiede esplicitamente di un autore terzo (es. "Cosa dice Gaito?"), tu rispondi assorbendo il concetto: "Nel mio approccio, ritengo che..." e dai la risposta senza citare l'autore.

ALTRE REGOLE:
- Non inventare nulla (no allucinazioni). Se la risposta non c'è nel contesto, di' "Non ho una risposta specifica su questo argomento nel mio database attuale."
- Usa un linguaggio professionale ma accessibile, frasi corte.
- Formatta la risposta in HTML per una migliore leggibilità (es. <b>grassetto</b>, <br> a capo, <ul><li>liste</li></ul>).

CONTESTO RECUPERATO DAL SECONDO CERVELLO DI DOMENICO:
{context}

DOMANDA DELL'UTENTE: {query}
"""
    # La scansione ha rivelato che i modelli 1.5 e 2.0 sono deprecati o bloccati sul free tier.
    # Usiamo l'alias stabile universale che Google aggiorna automaticamente all'ultimo Flash gratuito.
    available_model = 'gemini-2.5-flash'
                
    model = genai.GenerativeModel(available_model)
    
    # Come sopra, fail fast per migliorare la User Experience ed evitare caricamenti infiniti
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_str = str(e).lower()
        if "429" in error_str or "quota" in error_str:
            raise Exception("Hai superato il limite gratuito di Gemini (circa 15 richieste al minuto). Attendi circa 60 secondi e riprova!")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "Manca la domanda"}), 400
        
    try:
        
        # 1. Self-Querying: Estrai eventuale filtro per nome file
        file_filter = extract_file_filter(query)
        
        # 2. RAG Retrieval con o senza filtro
        context = get_retrieved_context(query, file_filter=file_filter)
        
        # 3. RAG Generation
        answer = generate_rag_answer(query, context)
        
        return jsonify({
            "answer": answer,
            "context": context,
            "filter_applied": file_filter
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n--- SERVER WEB DEL SECOND BRAIN AVVIATO ---")
    print("Vai su http://127.0.0.1:5000 dal tuo PC")
    print("O dal tuo cellulare usando l'IP locale del PC (es. http://192.168.1.X:5000)")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
