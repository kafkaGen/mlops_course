from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.routes import health, inference

load_dotenv(override=True)

app = FastAPI(title="Prompt Injection Classification")

app.include_router(inference.router)
app.include_router(health.router)
