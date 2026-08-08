from langchain_chroma import Chroma
from langchain_utils.embeddings import embeddings

# ---------------------------------
# Load Vector Database
# ---------------------------------

vector_store = Chroma(
    collection_name="research_papers",
    persist_directory="vector_db",
    embedding_function=embeddings
)

# ---------------------------------
# Retrieve Documents using MMR
# ---------------------------------
print("✅ RETRIEVER FILE LOADED")
def retrieve_documents(query):
    print("🔥 USING MMR RETRIEVER 🔥")
    documents = vector_store.max_marginal_relevance_search(
        query=query,
        k=5,
        fetch_k=20,
        lambda_mult=0.7
    )

    print("\n========== MMR RETRIEVAL ==========")

    print(f"Retrieved: {len(documents)}")

    for i, doc in enumerate(documents, start=1):

        print(f"\nChunk {i}")

        print(
            "SOURCE:",
            doc.metadata.get("source")
        )

        print(
            "CONTENT:",
            doc.page_content[:150]
        )

    print("\n===================================\n")

    return documents