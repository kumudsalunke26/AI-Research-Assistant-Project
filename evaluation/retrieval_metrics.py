"""
Phase 19.2
Retrieval Evaluation Metrics

Evaluates whether the expected source document
appears in the retrieved documents.
"""

from typing import List


def hit_rate_at_k(
    retrieved_sources: List[str],
    expected_source: str,
) -> float:

    if not expected_source:
        return 0.0

    expected_source = expected_source.lower()

    for source in retrieved_sources:

        if expected_source in source.lower():
            return 1.0

    return 0.0


def precision_at_k(
    retrieved_sources: List[str],
    expected_source: str,
) -> float:

    if not retrieved_sources or not expected_source:
        return 0.0

    expected_source = expected_source.lower()

    relevant = sum(
        1
        for source in retrieved_sources
        if expected_source in source.lower()
    )

    return relevant / len(retrieved_sources)


def recall_at_k(
    retrieved_sources: List[str],
    expected_source: str,
) -> float:

    if not expected_source:
        return 0.0

    expected_source = expected_source.lower()

    relevant = sum(
        1
        for source in retrieved_sources
        if expected_source in source.lower()
    )

    # For this evaluation dataset, one expected source
    # document is defined for each answerable question.
    return min(relevant, 1)


def evaluate_retrieval(
    retrieved_sources: List[str],
    expected_source: str,
):

    return {
        "hit_rate": hit_rate_at_k(
            retrieved_sources,
            expected_source,
        ),
        "precision": precision_at_k(
            retrieved_sources,
            expected_source,
        ),
        "recall": recall_at_k(
            retrieved_sources,
            expected_source,
        ),
    }