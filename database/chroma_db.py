import chromadb

# ---------------------------------
# Initialize ChromaDB
# ---------------------------------

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="research_papers"
)


# ---------------------------------
# Store Embeddings
# ---------------------------------

def store_embeddings(
    chunks,
    embeddings,
    file_name
):

    # Check if this file already exists
    existing = collection.get(
        where={
            "source": file_name
        }
    )

    if existing["ids"]:
        print(f"⚠️ {file_name} already exists. Skipping.")
        return

    # Unique IDs
    ids = [
        f"{file_name}_{i}"
        for i in range(len(chunks))
    ]

    # Store only chunk text
    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    # Store metadata
    metadatas = [
        {
            "source": file_name,
            "chunk_id": i,
            "page": chunk["page"]
        }
        for i, chunk in enumerate(chunks)
    ]

    # Add to Chroma
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # ---------------------------------
    # Debug Output
    # ---------------------------------

    print("\n========== DATABASE ==========")
    print("Stored File :", file_name)
    print("Total Vectors :", collection.count())

    data = collection.get()

    print("\nSample Metadata:")

    for metadata in data["metadatas"]:
     print(metadata)

    print("==============================")