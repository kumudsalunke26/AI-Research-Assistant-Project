# from config.gemini import generate_content
# from prompts.qa_prompt import get_qa_prompt


# def answer_question(question, context, memory):

#     prompt = get_qa_prompt(
#         context,
#         question,
#         memory
#     )

#     return generate_content(prompt)

from config.gemini import generate_content
from prompts.qa_prompt import get_qa_prompt
from models.qa_response import QAResponse
from google.genai import types


def answer_question(question, context, memory):

    prompt = get_qa_prompt(
        context,
        question,
        memory
    )

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=QAResponse
    )

    response = generate_content(
        prompt,
        config=config
    )

    result = QAResponse.model_validate_json(response)

    # ============================================================
    # ENSURE SOURCE INFORMATION IS ALWAYS PRESENT
    # ============================================================

    if context and context.strip():
        result.sources = ["Document Context"]
    else:
        result.sources = []

    # ============================================================
    # ENSURE CONFIDENCE MATCHES THE ANSWER
    # ============================================================

    not_found_message = (
        "I couldn't find that information in the uploaded document."
    )

    if not_found_message.lower() in result.answer.lower():
        result.confidence = "low"

    elif result.answer.strip():
        result.confidence = "high"

    else:
        result.confidence = "low"

    return result