# from typing import TypedDict, List
# from langchain_core.documents import Document
# class GraphState(TypedDict):

#     # Current question
#     question: str

#     # Chat history
#     messages: List[dict]

#     # Rewritten query
#     search_query: str

#     # Retrieved docs
#     documents: List[Document]

#     # Context
#     context: str

#     # Memory
#     memory: str

#     # Tool selected
#     tool: str

#     # Final answer
#     answer: str



from typing import TypedDict, List

from langchain_core.documents import Document

from models.qa_response import QAResponse


class GraphState(TypedDict):

    # Current question
    question: str

    # Chat history
    messages: List[dict]

    # Rewritten query
    search_query: str

    # Retrieved docs
    documents: List[Document]

    # Context
    context: str

    # Memory
    memory: str

    # Tool selected
    tool: str

    # Final structured answer
    answer: QAResponse