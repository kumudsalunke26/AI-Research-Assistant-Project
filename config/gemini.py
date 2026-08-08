# import os
# import time
# from dotenv import load_dotenv
# from google import genai
# load_dotenv()
# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY")
# )
# MODELS = [
#     "gemini-3.1-flash-lite",
#     "gemini-3.5-flash",
#     "gemini-2.0-flash"
# ]
# def generate_content(prompt, config=None):

#     last_error = None

#     for model in MODELS:

#         try:

#             print(f"Trying model: {model}")

#             response = client.models.generate_content(
#                 model=model,
#                 contents=prompt,
#                 config=config
#             )

#             print(f"Using model: {model}")

#             return response.text

#         except Exception as e:

#             print(f"{model} failed: {e}")

#             last_error = e

#             time.sleep(2)

#     raise Exception(
#         f"All Gemini models failed.\n\nLast Error:\n{last_error}"
#     )


import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.0-flash"
]


def generate_content(prompt, config=None):

    last_error = None

    for model in MODELS:

        try:

            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )

            print(f"Using model: {model}")

            return response.text

        except Exception as e:

            print(f"{model} failed: {e}")

            last_error = e

            time.sleep(2)

    raise Exception(
        f"All Gemini models failed.\n\nLast Error:\n{last_error}"
    )