from pydantic import BaseModel, Field

from src.api.core.schemas import ClassificationOutput


class QueryRequest(BaseModel):
    prompt: str = Field(max_length=10_000)


class ResponseRequest(BaseModel):
    response: ClassificationOutput


class HealthResponse(BaseModel):
    status: str
