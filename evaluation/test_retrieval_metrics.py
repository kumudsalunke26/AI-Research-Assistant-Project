from evaluation.retrieval_metrics import evaluate_retrieval


print("\n========== PHASE 19.2 ==========")


retrieved = [
    "Kumud_Salunke_Resume_nagarro.pdf",
    "another_document.pdf",
    "research_paper.pdf",
    "notes.pdf",
    "sample.pdf",
]


expected = "Kumud_Salunke_Resume_nagarro.pdf"


metrics = evaluate_retrieval(
    retrieved,
    expected,
)


print("Retrieved documents:")

for source in retrieved:
    print("-", source)


print("\nExpected source:")
print(expected)


print("\nMetrics:")

print(
    "Hit Rate:",
    metrics["hit_rate"]
)

print(
    "Precision:",
    metrics["precision"]
)

print(
    "Recall:",
    metrics["recall"]
)


print("\n==============================")