# AI-Powered Second Brain (RAG System)

Benvenuto in **Second Brain RAG**, un'architettura completa per interrogare e navigare enormi quantità di materiale didattico (video, presentazioni, pdf) utilizzando l'Intelligenza Artificiale.

## 📌 Il Problema
Avere decine di gigabyte di videocorsi e slide rende impossibile trovare un'informazione specifica senza dover riguardare ore di contenuti.
L'obiettivo di questo progetto è comprimere ore di formazione video in una Knowledge Base testuale e interrogarla in linguaggio naturale (Semantic Search).

## 💡 L'Architettura (V2)
Questo repository contiene la "Fase 2" del progetto, un sistema **Retrieval-Augmented Generation (RAG) Avanzato**:

1. **Ingestion & Processing**: Modelli locali (come Whisper) trascrivono e processano i file video/audio in file di testo raw.
2. **Vector Database**: Utilizzo di **ChromaDB** per l'archiviazione dei blocchi di testo.
3. **Local Embeddings**: Utilizzo di `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`) in locale per generare gli embedding a costo zero e in totale privacy.
4. **Fuzzy Search & Filtering**: Algoritmi di fuzzy matching per filtrare i metadati prima della ricerca vettoriale (es. ricercare solo nei file di uno specifico "Autore").
5. **Generazione AI (Gemini)**: Utilizzo delle API di Google Gemini (`gemini-2.5-flash`) per la sintesi finale e la stesura delle risposte, con un sistema di "Fail-Fast" per gestire i Rate Limit (errore 429).
6. **Frontend**: Un'app Web creata con Flask, dotata di UI/UX curata e responsiva per l'accesso da smartphone e LAN.

## 🚀 Come testarlo (Per Recruiter)

> **Nota per la Sicurezza**: Il repository non contiene il mio materiale protetto da copyright né le mie chiavi API (bloccati da `.gitignore`).

Ho fornito una cartella `example_data/` con un file testuale generico. Puoi usare questo per testare l'algoritmo di RAG:

1. Clona il repository.
2. Installa le dipendenze: `pip install -r requirements.txt`.
3. Crea un file `.env` e inserisci la tua chiave di Google AI Studio: `GEMINI_API_KEY=LaTuaChiave`
4. Metti i tuoi file di testo `.txt` nella cartella `output/` (puoi usare quello di esempio che ho fornito).
5. Avvia il server: `python server.py`.
6. Apri `http://127.0.0.1:5000` nel browser.

## 🔮 Evoluzione (V3 - Karpathy LLM Wiki Pattern)
Come naturale prosecuzione di questo progetto, la mia architettura si sta evolvendo verso un pattern **LLM Wiki**. Invece di recuperare blocchi di testo sparsi e sintetizzarli *on-the-fly* (RAG tradizionale), l'AI processa preventivamente i documenti per generare una "Enciclopedia Viva" (un grafo di file Markdown collegati), offrendo latenze quasi nulle e zero allucinazioni.
