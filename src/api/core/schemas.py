from pydantic import BaseModel


class ClassificationOutput(BaseModel):
    is_injection: bool
    injection_probability: float
    threshold: float
