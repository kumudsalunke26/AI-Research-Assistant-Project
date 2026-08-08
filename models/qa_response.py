from pydantic import BaseModel, Field


class QAResponse(BaseModel):

    answer: str = Field(
        description="The final answer to the user's question based only on the provided context."
    )

    sources: list[str] = Field(
        description="Names of source documents used to answer the question."
    )

    confidence: str = Field(
        description="Confidence level of the answer: high, medium, or low."
    )