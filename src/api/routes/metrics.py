from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Histogram, generate_latest
from starlette.responses import Response

router = APIRouter()
registry = CollectorRegistry()

# Per-minute metrics
PI_REQUEST_COUNT = Counter(
    "prompt_injection_requests_total",
    "Total prompt injection classification requests per minute",
    registry=registry,
)

PI_REQUEST_LATENCY = Histogram(
    "prompt_injection_latency_seconds",
    "Request latency histogram (in seconds) grouped by minute",
    registry=registry,
)

PI_ERROR_RATE = Counter(
    "prompt_injection_errors_total",
    "Total number of errors grouped by 5-minute blocks and error type",
    ["error_type"],
    registry=registry,
)

PI_CLASS_DISTRIBUTION = Counter(
    "prompt_injection_class_distribution_total",
    "Distribution of predicted classes per minute",
    ["class_label"],
    registry=registry,
)

PI_CONFIDENCE_DISTRIBUTION = Histogram(
    "prompt_injection_confidence_distribution",
    "Histogram of prediction confidence scores per minute",
    buckets=[0.2, 0.4, 0.6, 0.8, 1.0],
    registry=registry,
)


@router.get("/metrics")
def metrics():
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)


def record_prompt_injection_prediction_metrics(
    latency_seconds: float,
    predicted_class: str,
    confidence_score: float,
    is_error: bool = False,
    error_type: str = "unknown",
) -> None:
    PI_REQUEST_COUNT.inc()
    PI_REQUEST_LATENCY.observe(latency_seconds)

    if is_error:
        PI_ERROR_RATE.labels(error_type=error_type).inc()
        return

    PI_CLASS_DISTRIBUTION.labels(class_label=predicted_class).inc()
    PI_CONFIDENCE_DISTRIBUTION.observe(confidence_score)
