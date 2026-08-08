from langchain_utils.loader import load_pdf
from langchain_utils.splitter import split_documents

docs = load_pdf("Kumud_Salunke_Resume_nagarro.pdf")

chunks = split_documents(docs)

print("Total Chunks:", len(chunks))

print()

print(chunks[0])