from fastapi import APIRouter

from src.api.routes.schemas import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/ping")
async def ping() -> HealthResponse:
    return HealthResponse(status="OK")
