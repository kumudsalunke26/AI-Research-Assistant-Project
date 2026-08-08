# from config.gemini import generate_content
# def optimize_context(question, chunks):

#     context = "\n\n".join(chunks)

#     prompt = f"""
# You are a context optimization assistant.
# From the given context, extract ONLY information
# relevant to answering the question.
# Remove:
# - repeated information
# - unnecessary details
# - unrelated text
# Question:
# {question}
# Context:
# {context}
# Return only the optimized context.
# """

#     return generate_content(prompt)




from config.gemini import generate_content


def optimize_context(question, chunks):

    """
    Safely select relevant information from retrieved chunks.

    Important:
    - Do NOT invent information.
    - Do NOT rewrite facts.
    - Do NOT change numbers, names, technologies, or project details.
    - Preserve the original wording as much as possible.
    """

    context = "\n\n".join(chunks)

    prompt = f"""
You are a document-context selection assistant.

Your job is ONLY to select the parts of the provided context
that are relevant to answering the question.

STRICT RULES:

1. Use ONLY the provided context.
2. Do NOT use outside knowledge.
3. Do NOT invent information.
4. Do NOT rewrite or paraphrase facts.
5. Do NOT change numbers, names, technologies, dates, or project details.
6. Preserve important technical terms exactly as they appear.
7. If a project is mentioned, preserve all information directly
   related to that project.
8. If the question asks about technologies, preserve the complete
   technology list from the relevant project.
9. If the question asks about features, preserve all relevant
   feature information.
10. If the context contains relevant information, return it.
11. If nothing is relevant, return the original context unchanged.

Question:
{question}

Retrieved Context:
{context}

Return ONLY the relevant original information.
"""


    try:

        optimized = generate_content(prompt)

        if optimized and optimized.strip():

            return optimized.strip()

        return context

    except Exception as e:

        print("\n⚠️ CONTEXT OPTIMIZATION FAILED")
        print(e)

        # Critical safety fallback:
        # Never lose retrieved evidence because optimization failed.

        return context