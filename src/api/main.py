from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST

from src.api.routes import health, inference, metrics

load_dotenv(override=True)

app = FastAPI(title="Prompt Injection Classification")

app.include_router(inference.router)
app.include_router(health.router)
app.include_router(metrics.router)


@app.exception_handler(ValidationError)
async def custom_request_validation_handler(request: Request, exc: ValidationError):
    errors = [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "detail": "Pydantic Validation error",
            "errors": errors,
        },
    )
