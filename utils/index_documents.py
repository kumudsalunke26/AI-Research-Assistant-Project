
import os
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

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


# ============================================================
# TEXT SPLITTER
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


# ============================================================
# CREATE VECTOR STORE
# ============================================================

def create_vector_store():

    logger.info(
        "Creating/loading Chroma vector store."
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store


# ============================================================
# RESET VECTOR DATABASE
# ============================================================

def reset_vector_database():

    if os.path.exists(VECTOR_DB_PATH):

        logger.warning(
            "Deleting existing vector database: %s",
            VECTOR_DB_PATH
        )

        shutil.rmtree(VECTOR_DB_PATH)

    logger.info(
        "Vector database reset completed."
    )


# ============================================================
# INDEX DOCUMENTS
# ============================================================

def index_documents(documents):

    """
    Index LangChain Document objects into Chroma.

    Parameters
    ----------
    documents : list
        List of LangChain Document objects.

    Returns
    -------
    int
        Number of chunks indexed.
    """

    # --------------------------------------------------------
    # VALIDATE DOCUMENTS
    # --------------------------------------------------------

    if not documents:

        logger.warning(
            "No documents received for indexing."
        )

        return 0


    # --------------------------------------------------------
    # LOG INPUT DOCUMENTS
    # --------------------------------------------------------

    logger.info(
        "Received %d documents for indexing.",
        len(documents)
    )


    input_sources = {}

    for document in documents:

        metadata = getattr(
            document,
            "metadata",
            {}
        ) or {}

        source = metadata.get(
            "source",
            "unknown"
        )

        input_sources[source] = (
            input_sources.get(source, 0) + 1
        )


    logger.info(
        "Input document sources: %s",
        input_sources
    )


    # --------------------------------------------------------
    # CREATE / LOAD VECTOR STORE
    # --------------------------------------------------------

    vector_store = create_vector_store()


    # --------------------------------------------------------
    # SPLIT DOCUMENTS INTO CHUNKS
    # --------------------------------------------------------

    chunks = text_splitter.split_documents(
        documents
    )


    logger.info(
        "Created %d chunks from %d documents.",
        len(chunks),
        len(documents)
    )


    if not chunks:

        logger.warning(
            "Text splitting produced zero chunks."
        )

        return 0


    # --------------------------------------------------------
    # NORMALIZE METADATA
    # --------------------------------------------------------

    for index, chunk in enumerate(chunks):

        metadata = chunk.metadata or {}

        source = metadata.get(
            "source",
            "unknown"
        )

        page = metadata.get(
            "page",
            metadata.get(
                "page_number",
                None
            )
        )

        chunk.metadata = {
            "source": str(source),
            "page": page if page is not None else -1,
            "chunk_id": index
        }


    # --------------------------------------------------------
    # LOG CHUNK SOURCES
    # --------------------------------------------------------

    chunk_sources = {}

    for chunk in chunks:

        source = chunk.metadata.get(
            "source",
            "unknown"
        )

        chunk_sources[source] = (
            chunk_sources.get(source, 0) + 1
        )


    logger.info(
        "Chunks by source: %s",
        chunk_sources
    )


    # --------------------------------------------------------
    # CREATE UNIQUE IDS
    # --------------------------------------------------------

    ids = []

    for index, chunk in enumerate(chunks):

        source = Path(
            chunk.metadata["source"]
        ).stem

        page = chunk.metadata.get(
            "page",
            -1
        )

        chunk_id = (
            f"{source}_"
            f"{page}_"
            f"{index}"
        )

        ids.append(
            chunk_id
        )


    # --------------------------------------------------------
    # STORE DOCUMENT CHUNKS IN CHROMA
    # --------------------------------------------------------

    logger.info(
        "Adding %d chunks to Chroma.",
        len(chunks)
    )

    vector_store.add_documents(
        documents=chunks,
        ids=ids
    )


    logger.info(
        "Successfully indexed %d chunks.",
        len(chunks)
    )


    # --------------------------------------------------------
    # VERIFY DATABASE
    # --------------------------------------------------------

    data = vector_store.get(
        include=["metadatas"]
    )


    total_chunks = len(
        data.get("ids", [])
    )


    logger.info(
        "Chroma now contains %d chunks.",
        total_chunks
    )


    # --------------------------------------------------------
    # VERIFY SOURCES
    # --------------------------------------------------------

    sources = set()

    for metadata in data.get(
        "metadatas",
        []
    ):

        if metadata:

            sources.add(
                metadata.get(
                    "source",
                    "unknown"
                )
            )


    logger.info(
        "Indexed sources: %s",
        sorted(sources)
    )


    # --------------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------------

    logger.info(
        "========== VECTOR DATABASE VERIFICATION =========="
    )

    logger.info(
        "Total chunks: %d",
        total_chunks
    )

    logger.info(
        "Total sources: %d",
        len(sources)
    )

    for source in sorted(sources):

        logger.info(
            "Source: %s",
            source
        )

    logger.info(
        "==================================================="
    )


    return len(chunks)

