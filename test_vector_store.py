from langchain_utils.loader import load_pdf
from langchain_utils.splitter import split_documents
from langchain_utils.vector_store import create_vector_store

docs = load_pdf(
    "Kumud_Salunke_Resume_nagarro.pdf"
)

chunks = split_documents(docs)

db = create_vector_store(chunks)

print("Vector DB created successfully!")