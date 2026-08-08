from config.gemini import generate_content
from prompts.summary_prompt import get_summary_prompt


def summarize(context):

    prompt = get_summary_prompt(
        context
    )

    return generate_content(prompt)