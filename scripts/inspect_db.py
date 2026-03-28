import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="pp_recipes_knowledge")

results = collection.get(include=["documents"])

documents = results["documents"]
total_chunks = len(documents)  # type: ignore

print(f"📊 Всего кусков текста в базе: {total_chunks}\n")

if total_chunks > 0:
    print("=== ПЕРВЫЕ 3 ФРАГМЕНТА (Обычно тут аннотации и оглавление) ===")
    for i in range(min(3, total_chunks)):
        print(f"\n--- Чанк {i + 1} ---")
        print(documents[i][:300] + "...")  # type: ignore

    print(
        "\n\n=== ПОСЛЕДНИЕ 3 ФРАГМЕНТА (Обычно тут алфавитный указатель или заключение) ==="
    )
    for i in range(max(0, total_chunks - 3), total_chunks):
        print(f"\n--- Чанк {i + 1} ---")
        print(documents[i][:300] + "...")  # type: ignore
else:
    print("База пуста!")
