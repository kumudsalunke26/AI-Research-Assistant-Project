def get_router_prompt(question):

    return f"""
You are an AI Router.

Your job is to decide which tool should answer the user's request.

Available tools:

1. qa
Use for factual questions where the user wants information from the document.

2. summary
Use when the user asks for:
- summary
- overview
- abstract
- brief explanation

3. keyword
Use when the user asks for:
- keywords
- key terms
- important concepts
- topics


Return ONLY one word:

qa

OR

summary

OR

keyword


Question:

{question}
"""