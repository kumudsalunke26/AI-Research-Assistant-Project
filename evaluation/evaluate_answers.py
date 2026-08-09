"""
Phase 19.4
Answer / Generation Evaluation

Evaluates whether the generated answer contains
the important information from the expected answer.
"""

from evaluation.qa_dataset import EVALUATION_DATASET

from langchain_utils.retriever import retrieve_documents

from tools.qa_tool import answer_question


def build_context(documents):
    """
    Convert retrieved documents into text context.
    """

    chunks = []

    for document in documents:

        text = getattr(
            document,
            "page_content",
            ""
        )

        if text and text.strip():

            chunks.append(
                text.strip()
            )

    return "\n\n".join(chunks)


def normalize_text(text):
    """
    Normalize text for simple comparison.
    """

    if not text:
        return ""

    return (
        str(text)
        .lower()
        .replace(",", "")
        .replace(".", "")
        .replace(":", "")
        .replace(";", "")
        .replace("(", "")
        .replace(")", "")
        .replace("-", " ")
    )


def calculate_answer_coverage(
    generated_answer,
    expected_answer
):
    """
    Calculate how much of the expected answer
    is represented in the generated answer.

    This is a lightweight lexical evaluation,
    not a semantic judge.
    """

    if not expected_answer:
        return 0.0

    generated = normalize_text(
        generated_answer
    )

    expected = normalize_text(
        expected_answer
    )

    expected_words = [
        word
        for word in expected.split()
        if len(word) > 2
    ]

    if not expected_words:
        return 0.0

    matched_words = 0

    for word in expected_words:

        if word in generated:

            matched_words += 1

    coverage = (
        matched_words /
        len(expected_words)
    )

    return coverage


def check_hallucination_refusal(answer):
    """
    Check whether the system refuses to answer
    when the information is unavailable.
    """

    if not answer:
        return False

    answer = str(answer).lower()

    refusal_phrases = [

        "couldn't find",
        "could not find",
        "not found",
        "don't have",
        "do not have",
        "no information",
        "information is not available",
        "not mentioned",
        "not provided",
        "cannot determine",
        "can't determine",
        "unable to find",
    ]

    for phrase in refusal_phrases:

        if phrase in answer:

            return True

    return False


def main():

    print("\n")
    print("==============================================")
    print("       PHASE 19.4 ANSWER EVALUATION")
    print("==============================================")

    total_answerable = 0

    passed_answers = 0

    total_coverage = 0.0

    # ======================================================
    # PROCESS EACH EVALUATION QUESTION
    # ======================================================

    for item in EVALUATION_DATASET:

        question = item["question"]

        expected_answer = item["expected_answer"]

        expected_source = item["expected_source"]

        print("\n")
        print("----------------------------------------------")

        print(
            "ID:",
            item["id"]
        )

        print(
            "Question:",
            question
        )

        # ==================================================
        # UNANSWERABLE QUESTION
        # ==================================================

        if expected_answer is None:

            print(
                "Type: UNANSWERABLE"
            )

            print(
                "Expected behavior:"
            )

            print(
                "System should refuse rather than hallucinate."
            )

            try:

                documents = retrieve_documents(
                    question
                )

                context = build_context(
                    documents
                )

                answer = answer_question(
                    question,
                    context,
                    ""
                )

                print(
                    "\nGenerated answer:"
                )

                print(answer)

                refused = check_hallucination_refusal(
                    answer
                )

                if refused:

                    print(
                        "\n✅ PASS"
                    )

                    print(
                        "System correctly avoided hallucination."
                    )

                else:

                    print(
                        "\n⚠️ REVIEW"
                    )

                    print(
                        "The answer may require manual hallucination review."
                    )

            except Exception as e:

                print(
                    "\n❌ ERROR:"
                )

                print(e)

            continue

        # ==================================================
        # ANSWERABLE QUESTION
        # ==================================================

        total_answerable += 1

        print(
            "Expected source:",
            expected_source
        )

        print(
            "Expected answer:",
            expected_answer
        )

        try:

            # ----------------------------------------------
            # RETRIEVAL
            # ----------------------------------------------

            documents = retrieve_documents(
                question
            )

            print(
                "\nRetrieved documents:",
                len(documents)
            )

            # ----------------------------------------------
            # BUILD CONTEXT
            # ----------------------------------------------

            context = build_context(
                documents
            )

            print(
                "Context characters:",
                len(context)
            )

            # ----------------------------------------------
            # GENERATE ANSWER
            # ----------------------------------------------

            answer = answer_question(
                question,
                context,
                ""
            )

            print(
                "\nGenerated answer:"
            )

            print(answer)

            # ----------------------------------------------
            # COVERAGE
            # ----------------------------------------------

            coverage = calculate_answer_coverage(
                answer,
                expected_answer
            )

            print(
                "\nAnswer coverage:",
                round(coverage, 3)
            )

            # ----------------------------------------------
            # PASS / FAIL
            #
            # 50% coverage is used as a simple baseline.
            # ----------------------------------------------

            if coverage >= 0.50:

                print(
                    "✅ PASS"
                )

                passed_answers += 1

            else:

                print(
                    "❌ FAIL"
                )

            total_coverage += coverage

        except Exception as e:

            print(
                "\n❌ EVALUATION ERROR:"
            )

            print(e)

    # ======================================================
    # OVERALL RESULTS
    # ======================================================

    print("\n")
    print("==============================================")
    print("             OVERALL RESULTS")
    print("==============================================")

    print(
        "Answerable questions:",
        total_answerable
    )

    print(
        "Passed answers:",
        passed_answers
    )

    if total_answerable > 0:

        pass_rate = (
            passed_answers /
            total_answerable
        )

        average_coverage = (
            total_coverage /
            total_answerable
        )

        print(
            "Answer pass rate:",
            round(pass_rate, 3)
        )

        print(
            "Average answer coverage:",
            round(average_coverage, 3)
        )

    print(
        "=============================================="
    )

    print(
        "\n✅ PHASE 19.4 EVALUATION COMPLETE"
    )


if __name__ == "__main__":

    main()