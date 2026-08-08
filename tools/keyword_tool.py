import json
from config.gemini import generate_content
from prompts.keyword_prompt import get_keyword_prompt


def extract_keywords(context):

    prompt = get_keyword_prompt(context)

    response = generate_content(prompt)

    response = (
        response.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        data = json.loads(response)
        return data["keywords"]

    except Exception:

        keywords = []

        for line in response.split("\n"):

            line = line.replace("-", "").replace("•", "").strip()

            if line:
                keywords.append(line)

        return keywords