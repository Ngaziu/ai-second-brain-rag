import chromadb
from chromadb.utils import embedding_functions

db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"
client = chromadb.PersistentClient(path=db_dir)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2")
collection = client.get_collection(name="second_brain_collection", embedding_function=emb_fn)

docs = collection.get(include=["metadatas"])
sources = set()
for meta in docs['metadatas']:
    if meta and 'source' in meta:
        sources.add(meta['source'])

print(f"Total documents in DB: {len(docs['ids'])}")
print(f"Total unique sources: {len(sources)}")

print("\nSearching for 'talent' in sources (case-insensitive):")
found = False
for s in sources:
    if 'talent' in s.lower() or 'garden' in s.lower() or 'ui' in s.lower():
        print(f"- {s}")
        found = True

if not found:
    print("NO SOURCE FOUND containing 'talent', 'garden' or 'ui'!")
