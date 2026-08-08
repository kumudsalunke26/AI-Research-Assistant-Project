def get_recent_history(messages, limit=4):

    history = ""

    for msg in messages[-limit:]:

        history += (
            f"{msg['role']}: "
            f"{msg['content']}\n"
        )

    return history