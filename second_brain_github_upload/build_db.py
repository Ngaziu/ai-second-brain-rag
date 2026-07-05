import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
input_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\output"
db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"

def build_vector_db():
    print("--- INIZIO COSTRUZIONE VECTOR DATABASE ---")
    
    # 1. Inizializza ChromaDB persistente
    client = chromadb.PersistentClient(path=db_dir)
    
    # 2. Setup Embedding Function (usiamo un modello locale leggero ma potente per l'italiano/inglese)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    # 3. Crea o ottieni la collection (tabella)
    collection = client.get_or_create_collection(
        name="second_brain_collection", 
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"} # Buona prassi per RAG
    )
    
    # 4. Inizializza il Chunker
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, # 500 caratteri per avere info dense ma mirate
        chunk_overlap=50, # Sovrapposizione per non tagliare concetti a meta'
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # 5. Processa i file di testo
    txt_files = glob.glob(os.path.join(input_dir, "*.txt"))
    print(f"Trovati {len(txt_files)} file da analizzare.")
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    for file_path in txt_files:
        basename = os.path.basename(file_path)
        print(f"Processando {basename}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            
        chunks = text_splitter.split_text(text)
        
        for i, chunk in enumerate(chunks):
            # Prepariamo i dati per Chroma
            chunk_id = f"{basename}_chunk_{i}"
            metadata = {"source": basename, "chunk_index": i}
            
            all_chunks.append(chunk)
            all_metadatas.append(metadata)
            all_ids.append(chunk_id)

    # 6. Salvataggio nel Database in batch (Chroma consiglia max 41666 per batch ma noi stiamo bassi per sicurezza)
    print(f"\nCaricamento di {len(all_chunks)} chunk nel database...")
    batch_size = 5000
    for i in range(0, len(all_chunks), batch_size):
        end_idx = min(i + batch_size, len(all_chunks))
        collection.upsert(
            documents=all_chunks[i:end_idx],
            metadatas=all_metadatas[i:end_idx],
            ids=all_ids[i:end_idx]
        )
        print(f"Salvato batch {i} -> {end_idx}...")

    print("\n=== DATABASE VETTORIALE CREATO CON SUCCESSO! ===")

if __name__ == "__main__":
    build_vector_db()
