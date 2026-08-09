# from graph.state import GraphState
# from agents.router import choose_tool
# from rag.query_rewriter import rewrite_query
# from memory.memory_manager import get_recent_history
# from rag.context_optimizer import optimize_context
# from rag.context_compressor import compress_context
# from tools.qa_tool import answer_question
# from tools.summary_tool import summarize
# from tools.keyword_tool import extract_keywords
# from memory.long_term_memory import search_memory
# def rewrite_query_node(state: GraphState):

#     history = get_recent_history(
#         state["messages"]
#     )

#     search_query = rewrite_query(
#         state["question"],
#         history
#     )

#     state["search_query"] = search_query
#     print("\n========== QUERY REWRITE ==========")
#     print("Original:", state["question"])
#     print("Rewritten:", search_query)
#     print("==================================")

#     return state

# from langchain_utils.retriever import retrieve_documents


# def retrieve_documents_node(state: GraphState):

#     documents = retrieve_documents(
#         state["search_query"]
#     )

#     print("Retrieved:", len(documents))

#     state["documents"] = documents

#     return state

# def build_context_node(state: GraphState):

#     # -------------------------
#     # Extract retrieved chunks
#     # -------------------------

#     retrieved_chunks = [
#         doc.page_content
#         for doc in state["documents"]
#     ]

#     # -------------------------
#     # Optimize Context
#     # -------------------------

#     context = optimize_context(
#         state["question"],
#         retrieved_chunks
#     )

#     # -------------------------
#     # Retrieve Memory
#     # -------------------------

#     memory = search_memory(
#         state["question"]
#     )

#     memory_context = "\n".join(memory)

#     # -------------------------
#     # Merge Memory
#     # -------------------------

#     context += f"""

# Previous User Memory:

# {memory_context}

# """

#     # -------------------------
#     # Compress Context
#     # -------------------------

#     context = compress_context(
#         context,
#         state["question"]
#     )

#     # -------------------------
#     # Save in State
#     # -------------------------

#     state["memory"] = memory_context

#     state["context"] = context
#     print("\n========== FINAL CONTEXT ==========")
#     print(state["context"][:1500])
#     print("===================================")
#     return state

# def router_node(state: GraphState):

#     tool = choose_tool(
#         state["question"]
#     )

#     print("Selected Tool:", tool)

#     state["tool"] = tool

#     return state

# def qa_node(state: GraphState):

#     answer = answer_question(
#         state["question"],
#         state["context"],
#         state["memory"]
#     )

#     state["answer"] = answer

#     return state

# def summary_node(state: GraphState):

#     answer = summarize(
#         state["context"]
#     )

#     state["answer"] = answer

#     return state

# def keyword_node(state: GraphState):

#     keywords = extract_keywords(
#         state["context"]
#     )

#     answer = "\n".join(
#         f"- {keyword}"
#         for keyword in keywords
#     )

#     state["answer"] = answer

#     return state




# from rag.context_manager import manage_context
# from graph.state import GraphState
# from agents.router import choose_tool
# from rag.query_rewriter import rewrite_query
# from memory.memory_manager import get_recent_history
# from rag.context_optimizer import optimize_context
# from rag.context_compressor import compress_context
# from tools.qa_tool import answer_question
# from tools.summary_tool import summarize
# from tools.keyword_tool import extract_keywords
# from memory.long_term_memory import search_memory
# def rewrite_query_node(state: GraphState):

#     history = get_recent_history(
#         state["messages"]
#     )

#     search_query = rewrite_query(
#         state["question"],
#         history
#     )

#     state["search_query"] = search_query
#     print("\n========== QUERY REWRITE ==========")
#     print("Original:", state["question"])
#     print("Rewritten:", search_query)
#     print("==================================")

#     return state

# from langchain_utils.retriever import retrieve_documents


# def retrieve_documents_node(state: GraphState):

#     documents = retrieve_documents(
#         state["search_query"]
#     )

#     print("Retrieved:", len(documents))

#     state["documents"] = documents

#     return state



# def build_context_node(state: GraphState):

#     # ============================================================
#     # EXTRACT RETRIEVED DOCUMENT CHUNKS
#     # ============================================================

#     documents = state.get("documents", [])

#     retrieved_chunks = []

#     for doc in documents:

#         text = getattr(
#             doc,
#             "page_content",
#             ""
#         )

#         if text and text.strip():

#             retrieved_chunks.append(
#                 text.strip()
#             )

#     # ============================================================
#     # BUILD ORIGINAL DOCUMENT CONTEXT
#     # ============================================================

#     document_context = "\n\n".join(
#         retrieved_chunks
#     )

#     # ============================================================
#     # CONTEXT-WINDOW MANAGEMENT
#     #
#     # Deterministic character limit.
#     # No LLM rewriting of factual evidence.
#     # ============================================================

#     document_context = manage_context(
#         document_context
#     )

#     # ============================================================
#     # LONG-TERM MEMORY
#     # ============================================================

#     try:

#         memory = search_memory(
#             state["question"]
#         )

#     except Exception as e:

#         print(
#             "\n⚠️ LONG-TERM MEMORY ERROR:"
#         )

#         print(e)

#         memory = []

#     memory_context = "\n".join(
#         memory
#     )

#     # ============================================================
#     # SAVE MEMORY SEPARATELY
#     # ============================================================

#     state["memory"] = memory_context

#     # ============================================================
#     # DOCUMENT CONTEXT
#     #
#     # Keep document evidence separate from memory.
#     # ============================================================

#     state["context"] = document_context

#     # ============================================================
#     # DEBUG
#     # ============================================================

#     print(
#         "\n========== CONTEXT MANAGEMENT =========="
#     )

#     print(
#         "Retrieved chunks:",
#         len(retrieved_chunks)
#     )

#     print(
#         "Original context characters:",
#         len("\n\n".join(retrieved_chunks))
#     )

#     print(
#         "Final context characters:",
#         len(document_context)
#     )

#     print(
#         "Memory characters:",
#         len(memory_context)
#     )

#     print(
#         "\n========== FINAL DOCUMENT CONTEXT =========="
#     )

#     print(
#         document_context[:3000]
#     )

#     print(
#         "\n============================================"
#     )

#     return state

# def router_node(state: GraphState):

#     tool = choose_tool(
#         state["question"]
#     )

#     print("Selected Tool:", tool)

#     state["tool"] = tool

#     return state

# def qa_node(state: GraphState):

#     answer = answer_question(
#         state["question"],
#         state["context"],
#         state["memory"]
#     )

#     state["answer"] = answer

#     return state

# def summary_node(state: GraphState):

#     answer = summarize(
#         state["context"]
#     )

#     state["answer"] = answer

#     return state

# def keyword_node(state: GraphState):

#     keywords = extract_keywords(
#         state["context"]
#     )

#     answer = "\n".join(
#         f"- {keyword}"
#         for keyword in keywords
#     )

#     state["answer"] = answer

#     return state




from rag.context_manager import (
    manage_context,
    count_tokens
)

from graph.state import GraphState

from agents.router import choose_tool

from rag.query_rewriter import rewrite_query

from memory.memory_manager import get_recent_history

from tools.qa_tool import answer_question

from tools.summary_tool import summarize

from tools.keyword_tool import extract_keywords

from memory.long_term_memory import search_memory

from langchain_utils.retriever import retrieve_documents


# ============================================================
# QUERY REWRITING NODE
# ============================================================

def rewrite_query_node(state: GraphState):

    history = get_recent_history(
        state["messages"]
    )

    search_query = rewrite_query(
        state["question"],
        history
    )

    state["search_query"] = search_query

    print(
        "\n========== QUERY REWRITE =========="
    )

    print(
        "Original:",
        state["question"]
    )

    print(
        "Rewritten:",
        search_query
    )

    print(
        "=================================="
    )

    return state


# ============================================================
# RETRIEVAL NODE
# ============================================================

def retrieve_documents_node(state: GraphState):

    documents = retrieve_documents(
        state["search_query"]
    )

    print(
        "Retrieved:",
        len(documents)
    )

    state["documents"] = documents

    return state


# ============================================================
# CONTEXT MANAGEMENT NODE
# ============================================================

def build_context_node(state: GraphState):

    # ========================================================
    # EXTRACT RETRIEVED DOCUMENT CHUNKS
    # ========================================================

    documents = state.get(
        "documents",
        []
    )

    retrieved_chunks = []

    for doc in documents:

        text = getattr(
            doc,
            "page_content",
            ""
        )

        if text and text.strip():

            retrieved_chunks.append(
                text.strip()
            )

    # ========================================================
    # BUILD ORIGINAL DOCUMENT CONTEXT
    # ========================================================

    original_context = "\n\n".join(
        retrieved_chunks
    )

    # ========================================================
    # TOKEN-AWARE CONTEXT MANAGEMENT
    #
    # Primary limit:
    #       6000 tokens
    #
    # Additional safety limit:
    #       30000 characters
    #
    # No LLM rewriting of factual evidence.
    # ========================================================

    document_context = manage_context(
        original_context,
        max_tokens=6000,
        max_chars=30000
    )

    # ========================================================
    # LONG-TERM MEMORY
    # ========================================================

    try:

        memory = search_memory(
            state["question"]
        )

    except Exception as e:

        print(
            "\n⚠️ LONG-TERM MEMORY ERROR:"
        )

        print(e)

        memory = []

    memory_context = "\n".join(
        memory
    )

    # ========================================================
    # SAVE MEMORY SEPARATELY
    #
    # Memory is NOT mixed into document evidence.
    # ========================================================

    state["memory"] = memory_context

    # ========================================================
    # SAVE DOCUMENT CONTEXT
    # ========================================================

    state["context"] = document_context

    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print(
        "\n========== CONTEXT MANAGEMENT =========="
    )

    print(
        "Retrieved chunks:",
        len(retrieved_chunks)
    )

    print(
        "Original context characters:",
        len(original_context)
    )

    print(
        "Original context tokens:",
        count_tokens(original_context)
    )

    print(
        "Final context characters:",
        len(document_context)
    )

    print(
        "Final context tokens:",
        count_tokens(document_context)
    )

    print(
        "Memory characters:",
        len(memory_context)
    )

    print(
        "\n========== FINAL DOCUMENT CONTEXT =========="
    )

    print(
        document_context[:3000]
    )

    print(
        "\n============================================"
    )

    return state


# ============================================================
# ROUTER NODE
# ============================================================

def router_node(state: GraphState):

    tool = choose_tool(
        state["question"]
    )

    print(
        "Selected Tool:",
        tool
    )

    state["tool"] = tool

    return state


# ============================================================
# QA NODE
# ============================================================

def qa_node(state: GraphState):

    answer = answer_question(
        state["question"],
        state["context"],
        state["memory"]
    )

    state["answer"] = answer

    return state


# ============================================================
# SUMMARY NODE
# ============================================================

def summary_node(state: GraphState):

    answer = summarize(
        state["context"]
    )

    state["answer"] = answer

    return state


# ============================================================
# KEYWORD NODE
# ============================================================

def keyword_node(state: GraphState):

    keywords = extract_keywords(
        state["context"]
    )

    answer = "\n".join(
        f"- {keyword}"
        for keyword in keywords
    )

    state["answer"] = answer

    return state