from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import GraphState

from graph.nodes import (
    rewrite_query_node,
    retrieve_documents_node,
    build_context_node,
    router_node,
    qa_node,
    summary_node,
    keyword_node
)

graph = StateGraph(GraphState)

graph.add_node("rewrite", rewrite_query_node)
graph.add_node("retrieve", retrieve_documents_node)
graph.add_node("context", build_context_node)
graph.add_node("router", router_node)
graph.add_node("qa", qa_node)
graph.add_node("summary", summary_node)
graph.add_node("keyword", keyword_node)

graph.add_edge(START, "rewrite")
graph.add_edge("rewrite", "retrieve")
graph.add_edge("retrieve", "context")
graph.add_edge("context", "router")


def route_tool(state):
    return state["tool"]


graph.add_conditional_edges(
    "router",
    route_tool,
    {
        "qa": "qa",
        "summary": "summary",
        "keyword": "keyword"
    }
)

graph.add_edge("qa", END)
graph.add_edge("summary", END)
graph.add_edge("keyword", END)

workflow = graph.compile()