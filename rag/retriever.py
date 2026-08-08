import chromadb
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

db = chromadb.PersistentClient(path="vector_db")

collection = db.get_or_create_collection(
    name="research_papers"
)


def retrieve_chunks(question):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )

    question_embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    return results