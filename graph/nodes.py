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
        "\n========== RETRIEVAL =========="
    )

    print(
        "Retrieved documents:",
        len(documents)
    )

    # --------------------------------------------------------
    # SAVE DOCUMENTS
    # --------------------------------------------------------

    state["documents"] = documents

    # --------------------------------------------------------
    # EXTRACT SOURCE INFORMATION
    # --------------------------------------------------------

    sources = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        metadata = getattr(
            document,
            "metadata",
            {}
        ) or {}

        source = metadata.get(
            "source",
            "Unknown source"
        )

        page = metadata.get(
            "page",
            -1
        )

        chunk_id = metadata.get(
            "chunk_id",
            "Unknown chunk"
        )

        source_info = (
            f"Source: {source} | "
            f"Page: {page} | "
            f"Chunk: {chunk_id}"
        )

        sources.append(
            source_info
        )

        print(
            f"{index}. {source_info}"
        )

    # --------------------------------------------------------
    # SAVE SOURCES IN STATE
    # --------------------------------------------------------

    state["sources"] = sources

    print(
        "==============================\n"
    )

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
    # SAVE MEMORY
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


def qa_node(state: GraphState):

    documents = state.get(
        "documents",
        []
    )

    sources = []

    for document in documents:

        metadata = document.metadata or {}

        source = metadata.get(
            "source",
            "Unknown source"
        )

        page = metadata.get(
            "page",
            -1
        )

        chunk_id = metadata.get(
            "chunk_id",
            "Unknown chunk"
        )

        source_name = source.split("\\")[-1]

        citation = (
            f"{source_name} | "
            f"Page {page + 1} | "
            f"Chunk {chunk_id}"
        )

        if citation not in sources:
            sources.append(citation)

    answer = answer_question(
        state["question"],
        state["context"],
        state["memory"],
        sources=sources
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

