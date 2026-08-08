def manage_context(context, max_chars=12000):
    """
    Keep the context within a safe size limit.

    The current project uses character-based management rather
    than token counting. This is a simple safety layer before
    sending context to the LLM.
    """

    if not context:
        return ""

    context = context.strip()

    # Context is already within the limit
    if len(context) <= max_chars:
        print("\n========== CONTEXT WINDOW ==========")
        print("Original characters:", len(context))
        print("Final characters:", len(context))
        print("Context truncated: NO")
        print("=====================================")

        return context

    print("\n========== CONTEXT WINDOW ==========")
    print("Original characters:", len(context))
    print("Maximum characters:", max_chars)

    # --------------------------------------------------
    # Keep complete sections where possible.
    # --------------------------------------------------

    sections = context.split("\n\n")

    selected_sections = []
    current_length = 0

    for section in sections:

        section = section.strip()

        if not section:
            continue

        section_length = len(section)

        # Leave room for the section separator
        additional_length = section_length

        if selected_sections:
            additional_length += 2

        if current_length + additional_length > max_chars:
            break

        selected_sections.append(section)
        current_length += additional_length

    managed_context = "\n\n".join(selected_sections)

    # --------------------------------------------------
    # Safety fallback
    # --------------------------------------------------

    if not managed_context:

        managed_context = context[:max_chars]

    print("Final characters:", len(managed_context))
    print("Context truncated: YES")
    print("=====================================")

    return managed_context