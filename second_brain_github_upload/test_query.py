import chromadb
from chromadb.utils import embedding_functions

db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"
client = chromadb.PersistentClient(path=db_dir)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
collection = client.get_collection(name="second_brain_collection", embedding_function=emb_fn)

where_clause = {"$and": [{"source": {"$contains": "Talent"}}, {"source": {"$contains": "Garden"}}]}

results = collection.query(query_texts=["ui design"], n_results=5, where=where_clause)
print(f"Found {len(results['documents'][0])} documents with $and clause.")
for i in range(len(results['documents'][0])):
    print(results['metadatas'][0][i]['source'])
