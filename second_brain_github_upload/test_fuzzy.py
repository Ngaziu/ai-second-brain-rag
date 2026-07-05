import chromadb

def test_fuzzy():
    db_dir = r"C:\Users\Schip\.gemini\antigravity\scratch\second_brain_test\chroma_db"
    client = chromadb.PersistentClient(path=db_dir)
    collection = client.get_collection("second_brain_collection")
    
    docs = collection.get(include=["metadatas"])
    sources = set(m["source"] for m in docs["metadatas"] if m and "source" in m)
    
    print(f"Total unique sources: {len(sources)}")
    
    # Simulate user query keywords
    query_keywords = ["talent", "garden"]
    
    matched_sources = []
    for s in sources:
        s_lower = s.lower().replace("_", " ").replace("-", " ")
        if all(kw in s_lower for kw in query_keywords):
            matched_sources.append(s)
            
    print(f"\nMatched sources for {query_keywords}:")
    for m in matched_sources:
        print(f"- {m}")
        
    query_keywords = ["scalers"]
    matched_sources = []
    for s in sources:
        s_lower = s.lower().replace("_", " ").replace("-", " ")
        if all(kw in s_lower for kw in query_keywords):
            matched_sources.append(s)
            
    print(f"\nMatched sources for {query_keywords}:")
    for m in matched_sources:
        print(f"- {m}")

if __name__ == "__main__":
    test_fuzzy()
