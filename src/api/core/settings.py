from pydantic import Field
from pydantic_settings import BaseSettings


class PromptInjectionClassifierSettings(BaseSettings):
    model_registry_provider: str = Field("wandb", alias="MODEL_REGISTRY_PROVIDER")
    project_name: str = Field("model-registry", alias="MODEL_REGISTRY_PROJECT_NAME")
    model_name: str = Field("Prompt-injection-classifier", alias="MODEL_REGISTRY_MODEL_NAME")
    model_alias: str = Field("latest", alias="MODEL_REGISTRY_MODEL_ALIAS")
    threshold: float = Field(0.5, alias="INJECTION_THRESHOLD")
