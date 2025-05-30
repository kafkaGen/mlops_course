from pydantic import BaseModel

from src.api.core.schemas import ClassificationOutput


class QueryRequest(BaseModel):
    prompt: str


class ResponseRequest(BaseModel):
    response: ClassificationOutput


class HealthResponse(BaseModel):
    status: str
