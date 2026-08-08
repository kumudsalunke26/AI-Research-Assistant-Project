# from config.gemini import generate_content
# from prompts.router_prompt import get_router_prompt


# def choose_tool(question):
#     print("QUESTION:", question)
#     q = question.lower().strip()

#     # -------------------------
#     # Rule-Based Routing
#     # -------------------------

#     # Questions should always use QA
#     question_starters = (
#         "what",
#         "who",
#         "where",
#         "when",
#         "why",
#         "how",
#         "which",
#         "does",
#         "do",
#         "is",
#         "are",
#         "can",
#         "could",
#         "will",
#         "tell me",
#         "explain",
#         "describe"
#     )

#     if q.startswith(question_starters) or q.endswith("?"):
#         print("🛠 Router -> qa")
#         return "qa"

#     # Explicit summary requests
#     summary_words = [
#         "summary",
#         "summarize",
#         "summarise",
#         "overview",
#         "abstract"
#     ]

#     if any(word in q for word in summary_words):
#         print("🛠 Router -> summary")
#         return "summary"

#     # Explicit keyword requests
#     keyword_words = [
#         "keyword",
#         "keywords",
#         "key term",
#         "key terms",
#         "important term",
#         "important terms",
#         "concept",
#         "concepts"
#     ]

#     if any(word in q for word in keyword_words):
#         print("🛠 Router -> keyword")
#         return "keyword"

#     # -------------------------
#     # LLM Fallback
#     # -------------------------

#     prompt = get_router_prompt(question)

#     tool = (
#         generate_content(prompt)
#         .strip()
#         .lower()
#         .replace(".", "")
#     )

#     if tool not in ["qa", "summary", "keyword"]:
#         tool = "qa"

#     print(f"🛠 Router -> {tool}")

#     return tool




def choose_tool(question):

    q = question.lower().strip()

    # -------------------------
    # Summary
    # -------------------------
    if any(word in q for word in [
        "summary",
        "summarize",
        "summarise",
        "overview",
        "abstract"
    ]):
        print("🛠 Router -> summary")
        return "summary"

    # -------------------------
    # Keywords
    # -------------------------
    if any(word in q for word in [
        "keyword",
        "keywords",
        "key term",
        "key terms",
        "important term",
        "important terms",
        "concept",
        "concepts"
    ]):
        print("🛠 Router -> keyword")
        return "keyword"

    # -------------------------
    # Everything else -> QA
    # -------------------------
    print("🛠 Router -> qa")
    return "qa"