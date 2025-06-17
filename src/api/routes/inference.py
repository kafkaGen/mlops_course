import time

from fastapi import APIRouter, Depends

from src.api.core.prompt_injection_classifier import PromptInjectionClassifier
from src.api.core.settings import PromptInjectionClassifierSettings
from src.api.routes.metrics import record_prompt_injection_prediction_metrics
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
    start_time = time.time()

    try:
        output = prompto_injection_classifier.predict(request.prompt)
        processing_time = time.time() - start_time

        record_prompt_injection_prediction_metrics(
            latency_seconds=processing_time,
            predicted_class="Injected" if output.is_injection else "Not Injected",
            confidence_score=output.injection_probability,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        record_prompt_injection_prediction_metrics(
            latency_seconds=processing_time,
            predicted_class="",
            confidence_score=0.0,
            is_error=True,
            error_type=type(e).__name__,
        )
        raise

    return ResponseRequest(response=output)
