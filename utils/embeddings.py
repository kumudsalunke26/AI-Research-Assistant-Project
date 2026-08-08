import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def create_embeddings(chunks):

    embeddings = []

    for chunk in chunks:

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk["text"]
        )

        embeddings.append(
            response.embeddings[0].values
        )

    return embeddings