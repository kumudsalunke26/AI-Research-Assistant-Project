

# from langchain_chroma import Chroma

# from langchain_utils.embeddings import embeddings


# # ============================================================
# # CONFIGURATION
# # ============================================================

# VECTOR_DB_PATH = "vector_db"
# COLLECTION_NAME = "research_papers"


# # ============================================================
# # CREATE VECTOR STORE
# # ============================================================

# def create_vector_store(documents):
#     """
#     Create and persist a Chroma vector store.

#     Parameters
#     ----------
#     documents : list
#         List of LangChain Document objects.

#     Returns
#     -------
#     Chroma
#         Persisted Chroma vector store.
#     """

#     vector_store = Chroma.from_documents(
#         documents=documents,
#         embedding=embeddings,
#         collection_name=COLLECTION_NAME,
#         persist_directory=VECTOR_DB_PATH
#     )

#     return vector_store



from langchain_chroma import Chroma

from langchain_utils.embeddings import embeddings


VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "research_papers"


def create_vector_store(documents):

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    # Add documents with their existing metadata
    vector_store.add_documents(
        documents=documents
    )

    return vector_store