import chromadb
from chromadb.utils import embedding_functions
import math

def test_db():
    db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"
    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_collection("second_brain_collection")
    
    total_docs = collection.count()
    print(f"Total documents: {total_docs}")
    
    batch_size = 500
    batches = math.ceil(total_docs / batch_size)
    
    sources = set()
    for i in range(batches):
        docs = collection.get(limit=batch_size, offset=i*batch_size, include=["metadatas"])
        for m in docs["metadatas"]:
            if m and "source" in m:
                sources.add(m["source"])
                
    print(f"Total unique sources: {len(sources)}")
    
    print("\nLooking for 'talent' or 'garden':")
    for s in sources:
        if 'talent' in s.lower() or 'garden' in s.lower():
            print(f"- {s}")

if __name__ == "__main__":
    test_db()
