


import os
import chromadb
from dotenv import load_dotenv
from google import genai

from utils.logger import get_logger


# ============================================================
# LOGGER
# ============================================================

logger = get_logger(__name__)


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set in the environment variables."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# CHROMADB
# ============================================================

VECTOR_DB_PATH = "vector_db"
COLLECTION_NAME = "research_papers"

db = chromadb.PersistentClient(
    path=VECTOR_DB_PATH
)

collection = db.get_or_create_collection(
    name=COLLECTION_NAME
)


# ============================================================
# RETRIEVE CHUNKS
# ============================================================

def retrieve_chunks(question, k=5):
    """
    Retrieve the most relevant document chunks for a question.

    Parameters
    ----------
    question : str
        User's question.

    k : int
        Number of chunks to retrieve.

    Returns
    -------
    list
        Retrieved chunks containing:
        - content
        - metadata
        - distance
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question or not question.strip():
        logger.warning(
            "Empty question received for retrieval."
        )
        return []

    # --------------------------------------------------------
    # Validate k
    # --------------------------------------------------------

    if k <= 0:
        logger.warning(
            "Invalid k=%s. Using k=5.",
            k
        )
        k = 5

    try:

        logger.info(
            "Starting retrieval for question: %s",
            question
        )

        # ----------------------------------------------------
        # Generate question embedding
        # ----------------------------------------------------

        logger.info(
            "Generating question embedding using Gemini."
        )

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=question
        )

        question_embedding = response.embeddings[0].values

        logger.info(
            "Question embedding generated successfully."
        )

        # ----------------------------------------------------
        # Retrieve chunks from ChromaDB
        # ----------------------------------------------------

        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=k
        )

        # ----------------------------------------------------
        # Extract results safely
        # ----------------------------------------------------

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        logger.info(
            "Retrieved %d document chunks.",
            len(documents)
        )

        # ----------------------------------------------------
        # Format retrieved chunks
        # ----------------------------------------------------

        retrieved_chunks = []

        for i, document in enumerate(documents):

            metadata = (
                metadatas[i]
                if i < len(metadatas)
                else {}
            )

            distance = (
                distances[i]
                if i < len(distances)
                else None
            )

            chunk = {
                "content": document,
                "metadata": metadata,
                "distance": distance
            }

            retrieved_chunks.append(chunk)

        # ----------------------------------------------------
        # Log retrieved sources
        # ----------------------------------------------------

        for i, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):

            source = chunk["metadata"].get(
                "source",
                "Unknown source"
            )

            logger.info(
                "Chunk %d retrieved from: %s",
                i,
                source
            )

        # ----------------------------------------------------
        # Return results
        # ----------------------------------------------------

        return retrieved_chunks

    except Exception as e:

        logger.exception(
            "Error while retrieving chunks: %s",
            e
        )

        return []