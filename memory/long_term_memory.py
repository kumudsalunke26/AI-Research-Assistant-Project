import chromadb


client = chromadb.PersistentClient(
    path="memory_db"
)


collection = client.get_or_create_collection(
    name="user_memory"
)


def save_memory(text):

    print("Saving memory:", text)

    collection.add(
        documents=[text],
        ids=[
            str(collection.count())
        ]
    )


def search_memory(query):

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    print("\n========== MEMORY ==========")
    print(results)
    print("============================")

    return results["documents"][0]