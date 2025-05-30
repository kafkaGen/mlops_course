import tempfile

import fasttext

import wandb
from src.api.logger import logger


def pull_classification_model(
    model_name: str,
    model_alias: str,
    project_name: str | None = None,
    model_registry_provider: str = "wandb",
) -> fasttext.FastText:
    if model_registry_provider == "wandb":
        api = wandb.Api()

        if project_name is None:
            raise ValueError("Project name is required for wandb model registry provider.")

        artifact_path = f"{project_name}/{model_name}:{model_alias}"
        artifact = api.artifact(artifact_path)

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                model_path = artifact.get_entry("fasttext_model.bin").download(root=temp_dir)
                model = fasttext.load_model(model_path)
        except Exception as e:
            logger.error(f"Failed to load model {artifact_path}: {e}")
            raise

        logger.info(f"Model {artifact_path} loaded successfully.")

        return model

    else:
        raise ValueError(f"Unknown model registry provider: {model_registry_provider}")
