# Manuale d'Uso: Second Brain RAG (v2.0)

Questo documento contiene tutte le istruzioni per configurare e avviare il tuo Second Brain (ora più sicuro e responsivo), e per aggiornarlo in futuro con nuovi corsi.

---

## 0. Configurazione Iniziale di Sicurezza (Solo la prima volta)
Per garantire la massima sicurezza ed evitare che la tua chiave API finisca in chiaro, ora utilizziamo un sistema a "cassaforte" basato su un file segreto:
1. Vai nella cartella del progetto (`C:\Users\Schip\Documents\Master_AI_Workspace\second_brain_v2`).
2. Troverai un file che si chiama esattamente `.env`. Aprilo con Blocco Note.
3. Sostituisci `INSERISCI_QUI_LA_TUA_CHIAVE_API` con la tua vera API Key di Gemini.
4. Salva e chiudi il file. (Il backend Python la leggerà da lì, mantenendo il frontend sicuro al 100%).
*Nota: Il codice è stato anche aggiornato internamente per utilizzare `gemini-2.5-flash`, un modello che bypassa i severi limiti giornalieri introdotti da Google per il piano gratuito.*

---

## 1. Avviare il Server Web

Ogni volta che vuoi usare il tuo Second Brain, devi prima accendere il "motore" (il server locale).
Apri il tuo terminale (PowerShell o Prompt dei Comandi) e copia-incolla in sequenza queste due righe (modificando il percorso `cd` se sposti la cartella):

```powershell
cd C:\Users\Schip\Documents\Master_AI_Workspace\second_brain_v2
python server.py
```

*Nota: finché il terminale resta aperto con il server in esecuzione, il tuo Second Brain è attivo.*

---

## 2. Accedere all'Interfaccia Web (Da PC e da Mobile)

Una volta avviato il server, hai due modi per accedere all'app:

**Opzione 1: Dal tuo PC**
Apri il tuo browser preferito (Chrome, Edge, Safari) e vai a questo indirizzo:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

**Opzione 2: Dal tuo Cellulare (Novità v2)**
Sei sdraiato sul divano e vuoi fare una domanda al tuo Second Brain? Puoi farlo!
1. Assicurati che PC e Cellulare siano connessi allo stesso WiFi.
2. Trova l'IP locale del tuo PC (solitamente è qualcosa tipo `192.168.1.X`).
3. Digita quell'IP nel browser del telefono aggiungendo la porta 5000: `http://192.168.1.X:5000/`

L'interfaccia mobile è stata completamente ottimizzata, con una grafica responsiva che adatta lo spazio e i pulsanti senza nascondere nulla. È stata persino sviluppata una funzione di Fallback Universale per il tasto "Copia" che aggira i blocchi di sicurezza dei browser mobile sulle connessioni locali.

---

## 3. Aggiungere Nuovi Corsi (Prompt per l'Agente AI)

Quando acquisti nuovi corsi e aggiungi nuove sottocartelle (con video, pdf, pptx) all'interno della cartella principale, **non devi rifare tutto da capo**. Il sistema usa un file (`progress.json`) che ricorda i file già elaborati.

Per farmi analizzare i nuovi file, apri una nuova chat con me (Antigravity) e forniscimi esattamente questo comando/prompt:

> "Ciao, ho aggiunto nuovi file (video, pdf, pptx) nelle sottocartelle del mio archivio corsi (indica qui il percorso corretto, es: `C:\Users\Schip\Documents\Master_AI_Workspace\second_brain_v2`).
> 
> Avvia l'estrazione e l'aggiornamento del database vettoriale (ChromaDB) eseguendo lo script di elaborazione.
> **ATTENZIONE (Regola di Ingaggio):** Ricordati di leggere il file `progress.json` e di configurare lo script per IGNORARE tutti i file già processati, concentrandoti SOLO ed esclusivamente sui file nuovi o mai elaborati. Lavora in 'Goal Mode' e avvisami quando il database è aggiornato."

Questo prompt mi darà tutte le istruzioni necessarie per agganciarmi al lavoro precedente senza bruciare risorse per rielaborare gli 80GB vecchi.
