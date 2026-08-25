
from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):

    session_id: str = Field(..., min_length=1)
    question: str = Field(..., min_length=1)

    @field_validator("session_id", "question")
    @classmethod
    def validate_not_blank(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace.")

        return value
