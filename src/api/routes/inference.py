from fastapi import APIRouter, Depends

from src.api.core.prompt_injection_classifier import PromptInjectionClassifier
from src.api.core.settings import PromptInjectionClassifierSettings
from src.api.routes.schemas import QueryRequest, ResponseRequest

prompto_injection_classifier = PromptInjectionClassifier(settings=PromptInjectionClassifierSettings())

router = APIRouter(
    prefix="/model",
    tags=["Inference"],
)


def get_query_params(prompt: str) -> QueryRequest:
    return QueryRequest(prompt=prompt)


@router.get("/inference")
async def inference(request: QueryRequest = Depends(get_query_params)) -> ResponseRequest:
    output = prompto_injection_classifier.predict(request.prompt)

    return ResponseRequest(response=output)
