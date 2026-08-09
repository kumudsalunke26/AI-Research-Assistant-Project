# def manage_context(context, max_chars=12000):
#     """
#     Keep the context within a safe size limit.

#     The current project uses character-based management rather
#     than token counting. This is a simple safety layer before
#     sending context to the LLM.
#     """

#     if not context:
#         return ""

#     context = context.strip()

#     # Context is already within the limit
#     if len(context) <= max_chars:
#         print("\n========== CONTEXT WINDOW ==========")
#         print("Original characters:", len(context))
#         print("Final characters:", len(context))
#         print("Context truncated: NO")
#         print("=====================================")

#         return context

#     print("\n========== CONTEXT WINDOW ==========")
#     print("Original characters:", len(context))
#     print("Maximum characters:", max_chars)

#     # --------------------------------------------------
#     # Keep complete sections where possible.
#     # --------------------------------------------------

#     sections = context.split("\n\n")

#     selected_sections = []
#     current_length = 0

#     for section in sections:

#         section = section.strip()

#         if not section:
#             continue

#         section_length = len(section)

#         # Leave room for the section separator
#         additional_length = section_length

#         if selected_sections:
#             additional_length += 2

#         if current_length + additional_length > max_chars:
#             break

#         selected_sections.append(section)
#         current_length += additional_length

#     managed_context = "\n\n".join(selected_sections)

#     # --------------------------------------------------
#     # Safety fallback
#     # --------------------------------------------------

#     if not managed_context:

#         managed_context = context[:max_chars]

#     print("Final characters:", len(managed_context))
#     print("Context truncated: YES")
#     print("=====================================")

#     return managed_context




import tiktoken


# --------------------------------------------------
# Tokenizer
# --------------------------------------------------

def get_tokenizer():

    try:
        return tiktoken.get_encoding("cl100k_base")

    except Exception:
        return None


# --------------------------------------------------
# Count tokens
# --------------------------------------------------

def count_tokens(text):

    if not text:
        return 0

    tokenizer = get_tokenizer()

    if tokenizer is None:
        # Safe fallback
        return len(text) // 4

    return len(
        tokenizer.encode(
            text,
            disallowed_special=()
        )
    )


# --------------------------------------------------
# Token-aware context management
# --------------------------------------------------

def manage_context(
    context,
    max_tokens=6000,
    max_chars=30000
):

    """
    Keep the context within a safe token budget.

    The system uses token-aware management as the
    primary limit and a character limit as an
    additional safety layer.

    Complete sections are preserved whenever possible.
    """

    if not context:

        return ""

    context = context.strip()

    original_tokens = count_tokens(context)
    original_chars = len(context)

    # --------------------------------------------------
    # Context already within both limits
    # --------------------------------------------------

    if (
        original_tokens <= max_tokens
        and original_chars <= max_chars
    ):

        print("\n========== CONTEXT WINDOW ==========")

        print(
            "Original characters:",
            original_chars
        )

        print(
            "Original tokens:",
            original_tokens
        )

        print(
            "Maximum tokens:",
            max_tokens
        )

        print(
            "Maximum characters:",
            max_chars
        )

        print(
            "Final tokens:",
            original_tokens
        )

        print(
            "Final characters:",
            original_chars
        )

        print(
            "Context truncated: NO"
        )

        print(
            "=====================================",
        )

        return context

    # --------------------------------------------------
    # Select complete sections
    # --------------------------------------------------

    sections = context.split("\n\n")

    selected_sections = []

    current_tokens = 0
    current_chars = 0

    for section in sections:

        section = section.strip()

        if not section:
            continue

        section_tokens = count_tokens(section)
        section_chars = len(section)

        separator_tokens = (
            count_tokens("\n\n")
            if selected_sections
            else 0
        )

        separator_chars = (
            2
            if selected_sections
            else 0
        )

        new_token_count = (
            current_tokens
            + section_tokens
            + separator_tokens
        )

        new_char_count = (
            current_chars
            + section_chars
            + separator_chars
        )

        # --------------------------------------------------
        # Stop before exceeding either limit
        # --------------------------------------------------

        if new_token_count > max_tokens:
            break

        if new_char_count > max_chars:
            break

        selected_sections.append(section)

        current_tokens = new_token_count
        current_chars = new_char_count

    # --------------------------------------------------
    # Build managed context
    # --------------------------------------------------

    managed_context = "\n\n".join(
        selected_sections
    )

    # --------------------------------------------------
    # Safety fallback
    # --------------------------------------------------

    if not managed_context:

        tokenizer = get_tokenizer()

        if tokenizer:

            encoded = tokenizer.encode(
                context,
                disallowed_special=()
            )

            encoded = encoded[:max_tokens]

            managed_context = tokenizer.decode(
                encoded
            )

        else:

            managed_context = context[
                :max_chars
            ]

    final_tokens = count_tokens(
        managed_context
    )

    final_chars = len(
        managed_context
    )

    # --------------------------------------------------
    # Debug information
    # --------------------------------------------------

    print(
        "\n========== CONTEXT WINDOW =========="
    )

    print(
        "Original characters:",
        original_chars
    )

    print(
        "Original tokens:",
        original_tokens
    )

    print(
        "Maximum tokens:",
        max_tokens
    )

    print(
        "Maximum characters:",
        max_chars
    )

    print(
        "Final tokens:",
        final_tokens
    )

    print(
        "Final characters:",
        final_chars
    )

    print(
        "Context truncated: YES"
    )

    print(
        "====================================="
    )

    return managed_context