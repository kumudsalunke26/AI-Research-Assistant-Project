def get_summary_prompt(context):

    return f"""
You are an AI Research Assistant.

Your task:
Summarize the provided document context.

Rules:
1. Use ONLY the provided context.
2. Keep the summary concise.
3. Include:
   - Main objective
   - Important technologies/concepts
   - Key findings
4. Do not add information from outside.

Context:

{context}


Summary:
"""