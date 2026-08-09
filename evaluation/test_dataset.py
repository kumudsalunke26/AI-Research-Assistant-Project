from evaluation.qa_dataset import EVALUATION_DATASET


print("\n========== PHASE 19.1 ==========")

print(
    "Total evaluation questions:",
    len(EVALUATION_DATASET)
)

for item in EVALUATION_DATASET:

    print("\n------------------------------")

    print("ID:", item["id"])

    print("Question:", item["question"])

    print(
        "Expected source:",
        item["expected_source"]
    )

print("\n==============================")