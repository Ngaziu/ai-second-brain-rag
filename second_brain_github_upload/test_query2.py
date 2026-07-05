import chromadb
from chromadb.utils import embedding_functions

db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"
client = chromadb.PersistentClient(path=db_dir)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
collection = client.get_collection(name="second_brain_collection", embedding_function=emb_fn)

results = collection.query(query_texts=["Talent Garden UI Design"], n_results=50)

print("Top 50 matches:")
sources = set()
for i in range(len(results['documents'][0])):
    s = results['metadatas'][0][i]['source']
    sources.add(s)

for s in sources:
    print(f"- {s}")
