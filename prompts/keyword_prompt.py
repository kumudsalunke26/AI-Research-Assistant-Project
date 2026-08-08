def get_keyword_prompt(context):

    return f"""
Extract the 15 most important keywords from the following context.

Return ONLY valid JSON.

Format:

{{
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
  ]
}}

Context:

{context}
"""