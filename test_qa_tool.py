

from tools.qa_tool import answer_question
context = """
Kumud studies at MIT World Peace University.
Current CGPA: 9.05
Programming Languages:
Python
Java
JavaScript
"""
memory = ""
print(
    answer_question(
        "What is Kumud's cgpa?",
        context,
        memory
    )
)