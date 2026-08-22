from graph.workflow import workflow
from models.qa_response import QAResponse


# ============================================================
# INITIAL GRAPH STATE
# ============================================================

initial_state = {
    "question": "What are Kumud's skills?",
    "messages": [],
    "search_query": "",
    "documents": [],
    "context": "",
    "memory": "",
    "tool": "",
    "answer": None
}


# ============================================================
# RUN WORKFLOW
# ============================================================

print("\n========================================")
print("RUNNING AI RESEARCH ASSISTANT WORKFLOW")
print("========================================\n")

result = workflow.invoke(initial_state)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\n========================================")
print("WORKFLOW COMPLETED")
print("========================================")

print("\nOriginal Question:")
print(result["question"])

print("\nRewritten Query:")
print(result["search_query"])

print("\nSelected Tool:")
print(result["tool"])

print("\nRetrieved Documents:")
print(len(result["documents"]))

print("\nContext Length:")
print(len(result["context"]))

print("\n========================================")
print("FINAL ANSWER")
print("========================================")

answer = result["answer"]

if isinstance(answer, QAResponse):

    print("\nAnswer:")
    print(answer.answer)

    print("\nConfidence:")
    print(answer.confidence)

    print("\nSources:")
    print(answer.sources)

else:

    print(answer)

print("\n========================================")