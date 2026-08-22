


# from langchain_chroma import Chroma
# from langchain_utils.embeddings import embeddings

# from utils.logger import get_logger


# # ============================================================
# # LOGGER
# # ============================================================

# logger = get_logger(__name__)


# # ============================================================
# # LOAD VECTOR DATABASE
# # ============================================================

# vector_store = Chroma(
#     collection_name="research_papers",
#     persist_directory="vector_db",
#     embedding_function=embeddings
# )


# logger.info(
#     "Vector database loaded successfully."
# )


# # ============================================================
# # RETRIEVE DOCUMENTS USING MMR
# # ============================================================

# logger.info(
#     "MMR retriever initialized successfully."
# )


# def retrieve_documents(query):
#     """
#     Retrieve relevant documents using
#     Maximum Marginal Relevance (MMR).

#     Parameters
#     ----------
#     query : str
#         User's question.

#     Returns
#     -------
#     list
#         Retrieved LangChain documents.
#     """

#     # --------------------------------------------------------
#     # Validate query
#     # --------------------------------------------------------

#     if not query or not query.strip():

#         logger.warning(
#             "Empty query received for retrieval."
#         )

#         return []

#     try:

#         logger.info(
#             "Starting MMR retrieval."
#         )

#         logger.info(
#             "Query: %s",
#             query
#         )

#         # ----------------------------------------------------
#         # MMR Retrieval
#         # ----------------------------------------------------

#         documents = vector_store.max_marginal_relevance_search(
#             query=query,
#             k=5,
#             fetch_k=20,
#             lambda_mult=0.7
#         )

#         # ----------------------------------------------------
#         # Log retrieval count
#         # ----------------------------------------------------

#         logger.info(
#             "MMR retrieval completed. Retrieved %d documents.",
#             len(documents)
#         )

#         # ----------------------------------------------------
#         # Log retrieved sources
#         # ----------------------------------------------------

#         for i, doc in enumerate(
#             documents,
#             start=1
#         ):

#             source = doc.metadata.get(
#                 "source",
#                 "Unknown source"
#             )

#             logger.info(
#                 "Retrieved chunk %d from source: %s",
#                 i,
#                 source
#             )

#         # ----------------------------------------------------
#         # Existing console output
#         # ----------------------------------------------------

#         print("\n========== MMR RETRIEVAL ==========")

#         print(
#             f"Retrieved: {len(documents)}"
#         )

#         for i, doc in enumerate(
#             documents,
#             start=1
#         ):

#             print(
#                 f"\nChunk {i}"
#             )

#             print(
#                 "SOURCE:",
#                 doc.metadata.get("source")
#             )

#             print(
#                 "CONTENT:",
#                 doc.page_content[:150]
#             )

#         print(
#             "\n===================================\n"
#         )

#         # ----------------------------------------------------
#         # Return documents
#         # ----------------------------------------------------

#         return documents

#     except Exception as e:

#         logger.exception(
#             "Error during MMR retrieval: %s",
#             e
#         )

#         return []




from langchain_chroma import Chroma

from langchain_utils.embeddings import embeddings
from utils.logger import get_logger


# ============================================================
# LOGGER
# ============================================================

logger = get_logger(__name__)


# ============================================================
# CONFIGURATION
# ============================================================

VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "research_papers"

# Number of final documents returned
RETRIEVAL_K = 5

# Number of candidate documents considered before MMR selection
FETCH_K = 20

# MMR balance:
# 1.0 = more relevance
# 0.0 = more diversity
MMR_LAMBDA = 0.7


# ============================================================
# LOAD VECTOR DATABASE
# ============================================================

try:

    logger.info(
        "Loading Chroma vector database..."
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    logger.info(
        "Vector database loaded successfully."
    )

except Exception as e:

    logger.exception(
        "Failed to load vector database: %s",
        e
    )

    raise


# ============================================================
# VERIFY VECTOR DATABASE
# ============================================================

try:

    data = vector_store.get(
        include=["metadatas"]
    )

    total_chunks = len(
        data.get("ids", [])
    )

    logger.info(
        "Vector database contains %d chunks.",
        total_chunks
    )

except Exception as e:

    logger.exception(
        "Failed to verify vector database: %s",
        e
    )

    total_chunks = 0


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(query):
    """
    Retrieve relevant documents from Chroma
    using Maximum Marginal Relevance (MMR).

    Parameters
    ----------
    query : str
        User's search query.

    Returns
    -------
    list
        Retrieved LangChain Document objects.
    """

    # --------------------------------------------------------
    # VALIDATE QUERY
    # --------------------------------------------------------

    if not query or not query.strip():

        logger.warning(
            "Empty query received for retrieval."
        )

        return []

    query = query.strip()

    # --------------------------------------------------------
    # CHECK DATABASE
    # --------------------------------------------------------

    if total_chunks == 0:

        logger.warning(
            "Vector database is empty. "
            "Please run document ingestion first."
        )

        return []

    try:

        # ----------------------------------------------------
        # LOG QUERY
        # ----------------------------------------------------

        logger.info(
            "Starting MMR retrieval."
        )

        logger.info(
            "Query: %s",
            query
        )

        logger.info(
            "Retrieval configuration: k=%d, fetch_k=%d, lambda=%s",
            RETRIEVAL_K,
            FETCH_K,
            MMR_LAMBDA
        )

        # ----------------------------------------------------
        # MMR SEARCH
        # ----------------------------------------------------

        documents = vector_store.max_marginal_relevance_search(
            query=query,
            k=RETRIEVAL_K,
            fetch_k=FETCH_K,
            lambda_mult=MMR_LAMBDA
        )

        # ----------------------------------------------------
        # LOG RESULT COUNT
        # ----------------------------------------------------

        logger.info(
            "MMR retrieval completed. Retrieved %d documents.",
            len(documents)
        )

        # ----------------------------------------------------
        # LOG RETRIEVED DOCUMENTS
        # ----------------------------------------------------

        for index, document in enumerate(
            documents,
            start=1
        ):

            metadata = (
                document.metadata
                if document.metadata
                else {}
            )

            source = metadata.get(
                "source",
                "Unknown source"
            )

            page = metadata.get(
                "page",
                "Unknown page"
            )

            chunk_id = metadata.get(
                "chunk_id",
                "Unknown chunk"
            )

            logger.info(
                "Retrieved chunk %d | source=%s | page=%s | chunk_id=%s",
                index,
                source,
                page,
                chunk_id
            )

        # ----------------------------------------------------
        # RETURN DOCUMENTS
        # ----------------------------------------------------

        return documents

    except Exception as e:

        logger.exception(
            "Error during MMR retrieval: %s",
            e
        )

        return []

