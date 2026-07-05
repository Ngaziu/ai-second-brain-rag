import google.generativeai as genai
import sys

def test_filter(query):
    prompt = f"""Analizza la seguente domanda dell'utente e capisci se sta chiedendo di cercare informazioni all'interno di uno SPECIFICO file, corso o cartella.
Se sì, estrai SOLO le parole chiave più significative che potrebbero comporre il nome del file (es. se dice 'dal pdf Talent Garden', rispondi 'Talent_Garden' o 'Talent Garden').
Se non sta specificando una fonte precisa ma fa una domanda generale, rispondi ESATTAMENTE con la parola "NESSUNO".
Non aggiungere punteggiatura, non scrivere frasi complete. Solo le parole chiave o NESSUNO.

Domanda: {query}"""
    
    available_model = 'gemini-flash-latest'
    model = genai.GenerativeModel(available_model)
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    api_key = input("Inserisci API Key: ")
    genai.configure(api_key=api_key.strip())
    q = "estrai i concetti chiave dal pdf di talent garden e riportarli in 1000 parole"
    print("Filter estratto:", test_filter(q))
