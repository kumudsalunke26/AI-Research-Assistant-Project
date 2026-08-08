from utils.pdf_loader import extract_text
from utils.chunking import split_text

with open("Kumud_Salunke_Resume_nagarro.pdf", "rb") as f:

    pages = extract_text(f)

    chunks = split_text(pages)

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print("=" * 50)
    print("Chunk:", i)
    print("Page :", chunk["page"])
    print(chunk["text"][:120])