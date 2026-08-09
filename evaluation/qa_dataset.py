"""
Phase 19.1
RAG Evaluation Dataset

Contains questions, expected answers, and expected source documents.
This dataset will be used later to evaluate retrieval and QA quality.
"""


EVALUATION_DATASET = [

    {
        "id": "q01",
        "question": "Tell me about AURIS",
        "expected_answer": (
            "AURIS is a multilingual language processing system "
            "developed using Python and Hugging Face."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q02",
        "question": "What technologies did I use for AURIS?",
        "expected_answer": (
            "Python and Hugging Face."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q03",
        "question": "What are the features of AURIS?",
        "expected_answer": (
            "Language detection, translation, and speech processing "
            "across more than 10 languages."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q04",
        "question": "Tell me about RetailSphere",
        "expected_answer": (
            "RetailSphere is a Data Warehouse and Cloud Analytics "
            "Platform using Python, SQL, PostgreSQL, AWS S3, Boto3, "
            "and Power BI."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q05",
        "question": "How many records did RetailSphere process?",
        "expected_answer": (
            "RetailSphere processed more than 1.55 million records "
            "across nine datasets."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q06",
        "question": "What database architecture did RetailSphere use?",
        "expected_answer": (
            "A PostgreSQL data warehouse using a star-schema model "
            "with five dimension tables and a fact table."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q07",
        "question": "Tell me about JourneyStory",
        "expected_answer": (
            "JourneyStory was a full-stack platform where the candidate "
            "worked as a Full Stack Software Engineer Intern from "
            "November 2024 to May 2025."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q08",
        "question": "What technologies were used in JourneyStory?",
        "expected_answer": (
            "React.js, Firebase, and Cloudinary."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q09",
        "question": "What is Kumud's current CGPA?",
        "expected_answer": (
            "9.05 out of 10."
        ),
        "expected_source": "Kumud_Salunke_Resume_nagarro.pdf",
    },

    {
        "id": "q10",
        "question": "What is Kumud's favorite football team?",
        "expected_answer": None,
        "expected_source": None,
    },

]