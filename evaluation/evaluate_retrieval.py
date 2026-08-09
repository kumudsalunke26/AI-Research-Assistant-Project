"""
Phase 19.3
Real Retriever Evaluation

Runs the evaluation dataset through the project's
actual MMR retriever and calculates retrieval metrics.
"""

from evaluation.qa_dataset import EVALUATION_DATASET
from evaluation.retrieval_metrics import evaluate_retrieval
from langchain_utils.retriever import retrieve_documents


def get_source(document):
    """
    Extract the source filename from a retrieved document.
    """

    metadata = getattr(
        document,
        "metadata",
        {}
    )

    return metadata.get(
        "source",
        ""
    )


def main():

    print("\n")
    print("==============================================")
    print("       PHASE 19.3 RETRIEVAL EVALUATION")
    print("==============================================")

    total_questions = 0
    hit_total = 0.0
    precision_total = 0.0
    recall_total = 0.0

    for item in EVALUATION_DATASET:

        question = item["question"]
        expected_source = item["expected_source"]

        print("\n----------------------------------------------")
        print("ID:", item["id"])
        print("Question:", question)
        print("Expected source:", expected_source)

        # --------------------------------------------------
        # Unanswerable question
        # --------------------------------------------------

        if expected_source is None:

            print("Type: UNANSWERABLE")
            print("Skipping retrieval metric calculation.")

            continue

        # --------------------------------------------------
        # Retrieve using the REAL project retriever
        # --------------------------------------------------

        try:

            documents = retrieve_documents(
                question
            )

        except Exception as e:

            print("\n❌ RETRIEVAL ERROR")
            print(e)
            continue

        retrieved_sources = [
            get_source(doc)
            for doc in documents
        ]

        retrieved_sources = [
            source
            for source in retrieved_sources
            if source
        ]

        print("\nRetrieved sources:")

        for source in retrieved_sources:

            print(
                "-",
                source
            )

        # --------------------------------------------------
        # Calculate metrics
        # --------------------------------------------------

        metrics = evaluate_retrieval(
            retrieved_sources,
            expected_source
        )

        hit = metrics["hit_rate"]
        precision = metrics["precision"]
        recall = metrics["recall"]

        print("\nMetrics:")

        print(
            "Hit Rate:",
            hit
        )

        print(
            "Precision:",
            precision
        )

        print(
            "Recall:",
            recall
        )

        total_questions += 1

        hit_total += hit
        precision_total += precision
        recall_total += recall

    # ------------------------------------------------------
    # Overall results
    # ------------------------------------------------------

    print("\n")
    print("==============================================")
    print("             OVERALL RESULTS")
    print("==============================================")

    if total_questions == 0:

        print(
            "No answerable questions were evaluated."
        )

        return

    average_hit = (
        hit_total /
        total_questions
    )

    average_precision = (
        precision_total /
        total_questions
    )

    average_recall = (
        recall_total /
        total_questions
    )

    print(
        "Evaluated questions:",
        total_questions
    )

    print(
        "Average Hit Rate:",
        round(average_hit, 3)
    )

    print(
        "Average Precision:",
        round(average_precision, 3)
    )

    print(
        "Average Recall:",
        round(average_recall, 3)
    )

    print("==============================================")

    print("\n✅ RETRIEVAL EVALUATION COMPLETE")


if __name__ == "__main__":

    main()