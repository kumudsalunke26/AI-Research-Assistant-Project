from langchain_utils.retriever import retrieve_documents

docs = retrieve_documents(
    "What programming languages does Kumud know?"
)

print("Retrieved:", len(docs), "documents\n")

for i, doc in enumerate(docs, 1):
    print(f"Document {i}")
    print("-" * 40)
    print(doc.page_content)
    print(doc.metadata)
    print()