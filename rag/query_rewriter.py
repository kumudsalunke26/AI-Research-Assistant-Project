from config.gemini import generate_content


def rewrite_query(question, history):

    prompt = f"""
You are a query rewriting assistant.

Convert the user's question into a complete search query.

Use conversation history to understand references like:
- it
- this
- that
- they
- the second one

Conversation History:
{history}

Current Question:
{question}

Return only the rewritten search query.
"""

    return generate_content(prompt)