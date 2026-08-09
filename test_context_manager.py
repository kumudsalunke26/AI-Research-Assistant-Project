from rag.context_manager import (
    manage_context,
    count_tokens
)


context = """

AURIS is a multilingual language processing system.

It uses Python and Hugging Face.

It supports language detection, translation,
and speech processing across 10+ languages.

The system was tested through systematic testing
and iterative refinement.

It was deployed on Hugging Face Spaces.

"""


print(
    "\n========== ORIGINAL CONTEXT =========="
)

print(
    "Characters:",
    len(context)
)

print(
    "Tokens:",
    count_tokens(context)
)


managed_context = manage_context(
    context,
    max_tokens=50,
    max_chars=1000
)


print(
    "\n========== MANAGED CONTEXT =========="
)

print(
    managed_context
)

print(
    "======================================"
)

print(
    "\nFinal token count:",
    count_tokens(managed_context)
)

print(
    "Final character count:",
    len(managed_context)
)