"""
Phase 20
Evaluation Pipeline Runner

Runs the complete RAG evaluation pipeline:

1. Retrieval evaluation
2. Answer evaluation
3. Evaluation report
"""

import subprocess
import sys


# ============================================================
# RUN ONE EVALUATION STEP
# ============================================================

def run_step(module_name):
    """
    Run a Python evaluation module.

    Parameters
    ----------
    module_name : str
        Python module to execute.

    Returns
    -------
    bool
        True if the step succeeds, otherwise False.
    """

    print("\n")
    print("=" * 60)
    print("RUNNING:", module_name)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", module_name]
    )

    if result.returncode != 0:

        print("\n❌ STEP FAILED:", module_name)

        return False

    print("\n✅ STEP COMPLETE:", module_name)

    return True


# ============================================================
# MAIN EVALUATION PIPELINE
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("       PHASE 20 — FULL RAG EVALUATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Evaluation steps
    # --------------------------------------------------------

    steps = [

        "evaluation.evaluate_retrieval",

        "evaluation.evaluate_answers",

        "evaluation.evaluation_report",

    ]

    # --------------------------------------------------------
    # Run each step sequentially
    # --------------------------------------------------------

    for step in steps:

        success = run_step(step)

        if not success:

            print("\n❌ Evaluation pipeline stopped.")

            return

    # --------------------------------------------------------
    # Pipeline completed successfully
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("       ✅ FULL EVALUATION COMPLETE")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()