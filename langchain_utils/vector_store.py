from langchain_chroma import Chroma

from langchain_utils.embeddings import embeddings


def create_vector_store(documents):

    vector_store = Chroma.from_documents(

        documents=documents,

        embedding=embeddings,

        persist_directory="vector_db"

    )

    return vector_store