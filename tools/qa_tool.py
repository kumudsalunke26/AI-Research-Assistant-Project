
from config.gemini import generate_content
from prompts.qa_prompt import get_qa_prompt
from models.qa_response import QAResponse
from google.genai import types


def answer_question(question, context, memory, sources=None):
    """
    Generate a grounded answer using the retrieved document context.

    Parameters
    ----------
    question : str
        User's original question.

    context : str
        Retrieved document context.

    memory : str
        Relevant long-term memory.

    sources : list, optional
        Source information extracted from retrieved documents.

    Returns
    -------
    QAResponse
        Structured answer with confidence and sources.
    """

    # ============================================================
    # BUILD QA PROMPT
    # ============================================================

    prompt = get_qa_prompt(
        context,
        question,
        memory
    )

    # ============================================================
    # GEMINI STRUCTURED OUTPUT CONFIGURATION
    # ============================================================

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=QAResponse
    )

    # ============================================================
    # GENERATE ANSWER
    # ============================================================

    response = generate_content(
        prompt,
        config=config
    )

    # ============================================================
    # VALIDATE GEMINI RESPONSE
    # ============================================================

    try:
        result = QAResponse.model_validate_json(response)

    except Exception as e:

        print("\n========== QA RESPONSE ERROR ==========")
        print("Failed to parse Gemini response:")
        print(e)
        print("Raw response:")
        print(response)
        print("=======================================\n")

        return QAResponse(
            answer="I couldn't generate a valid answer from the uploaded document.",
            confidence="low",
            sources=sources or []
        )

    # ============================================================
    # SOURCE INFORMATION
    # ============================================================

    if sources:
        result.sources = sources

    elif context and context.strip():
        result.sources = ["Document Context"]

    else:
        result.sources = []

    # ============================================================
    # CONFIDENCE
    # ============================================================

    not_found_messages = [
        "I couldn't find that information in the uploaded document.",
        "I could not find that information in the uploaded document.",
        "I don't have enough information in the uploaded document.",
        "The uploaded document does not contain that information."
    ]

    answer_lower = result.answer.lower()

    if any(
        message.lower() in answer_lower
        for message in not_found_messages
    ):
        result.confidence = "low"

    elif result.answer.strip():
        result.confidence = "high"

    else:
        result.confidence = "low"

    # ============================================================
    # RETURN STRUCTURED RESPONSE
    # ============================================================

    return result

