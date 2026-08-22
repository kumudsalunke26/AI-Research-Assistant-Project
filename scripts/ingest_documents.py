
import sys
from pathlib import Path


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from langchain_utils.loader import load_pdf
from langchain_utils.splitter import split_documents
from langchain_utils.vector_store import create_vector_store


# ============================================================
# PDF PATH
# ============================================================

PDF_PATH = PROJECT_ROOT / "Kumud_Salunke_Resume_nagarro.pdf"


# ============================================================
# VALIDATE PDF
# ============================================================

if not PDF_PATH.exists():

    raise FileNotFoundError(
        f"PDF not found: {PDF_PATH}"
    )


# ============================================================
# LOAD PDF
# ============================================================

print("Loading PDF...")

docs = load_pdf(
    str(PDF_PATH)
)

print(
    f"Loaded {len(docs)} document pages."
)


# ============================================================
# SPLIT DOCUMENTS
# ============================================================

print("Splitting documents...")

chunks = split_documents(
    docs
)
print(f"Total chunks created: {len(chunks)}")
for index, chunk in enumerate(chunks):

    chunk.metadata["chunk_id"] = index
    chunk.metadata["source"] = str(PDF_PATH)
    chunk.metadata["page"] = chunk.metadata.get("page", -1)

print(
    f"Total chunks created: {len(chunks)}"
)


# ============================================================
# VALIDATE CHUNKS
# ============================================================

if not chunks:

    raise ValueError(
        "No chunks were created from the PDF."
    )


# ============================================================
# CREATE VECTOR DATABASE
# ============================================================

print("Creating vector database...")

db = create_vector_store(
    chunks
)

print(
    "Vector DB created successfully!"
)


# ============================================================
# VERIFY VECTOR DATABASE
# ============================================================

print("Verifying vector database...")

data = db.get(
    include=["metadatas"]
)

stored_ids = data.get(
    "ids",
    []
)

print(
    f"Total chunks stored in Chroma: {len(stored_ids)}"
)


# ============================================================
# SHOW FIRST CHUNK
# ============================================================

print("\nFirst chunk:")

print(
    chunks[0]
)


# ============================================================
# FINAL STATUS
# ============================================================

if len(stored_ids) == len(chunks):

    print(
        "\nSUCCESS: All chunks were stored in Chroma."
    )

else:

    print(
        "\nWARNING: Number of stored chunks does not "
        "match number of created chunks."
    )

