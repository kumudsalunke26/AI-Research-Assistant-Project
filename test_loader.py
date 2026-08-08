from langchain_utils.loader import load_pdf

docs = load_pdf("Kumud_Salunke_Resume_nagarro.pdf")

print(len(docs))

print(docs[0])