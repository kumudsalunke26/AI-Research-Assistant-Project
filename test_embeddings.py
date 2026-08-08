from langchain_utils.embeddings import embeddings

vector = embeddings.embed_query(
    "What programming languages does Kumud know?"
)

print(len(vector))

print(vector[:10])