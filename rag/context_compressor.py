from config.gemini import generate_content


def compress_context(context, question):

    prompt = f"""
You are a context optimization system.

Your task:
Extract ONLY the information relevant to the user's question.

Remove:
- repeated information
- unnecessary details
- unrelated content

Keep:
- important facts
- technical terms
- numbers
- names

Question:
{question}

Context:
{context}

Return only the optimized context.
"""

    return generate_content(prompt)