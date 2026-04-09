import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="pp_recipes_knowledge")

results = collection.get(include=["documents"])

documents = results["documents"]
total_chunks = len(documents)  # type: ignore

print(f"Total chunks in db: {total_chunks}\n")

if total_chunks > 0:
    print("=== First 3 framgents ===")
    for i in range(min(3, total_chunks)):
        print(f"\n--- Chunk {i + 1} ---")
        print(documents[i][:300] + "...")  # type: ignore

    print("\n\n=== Last 3 framgents ===")
    for i in range(max(0, total_chunks - 3), total_chunks):
        print(f"\n--- Chunk {i + 1} ---")
        print(documents[i][:300] + "...")  # type: ignore
else:
    print("No data!")
