import re

from src.api.core.schemas import ClassificationOutput
from src.api.core.settings import PromptInjectionClassifierSettings
from src.api.utils import pull_classification_model


class PromptInjectionClassifier:
    def __init__(
        self,
        settings: PromptInjectionClassifierSettings,
    ):
        self.settings = settings
        self.model = pull_classification_model(
            model_name=settings.model_name,
            model_alias=settings.model_alias,
            project_name=settings.project_name,
            model_registry_provider=settings.model_registry_provider,
        )

    def prompt_preprocess(self, prompt: str) -> str:
        prompt = prompt.strip().lower()
        prompt = re.sub(r"[^\w\s]", "", prompt)
        prompt = re.sub(r"\s+", " ", prompt).strip()
        return prompt

    def predict(self, prompt: str) -> ClassificationOutput:
        prompt = self.prompt_preprocess(prompt)

        labels, probs = self.model.predict(prompt, k=2)
        label_mapping = {label.replace("__label__", ""): prob for label, prob in zip(labels, probs)}
        is_injection = label_mapping.get("Injection", 0) > self.settings.threshold

        return ClassificationOutput(
            is_injection=is_injection,
            injection_probability=float(label_mapping.get("Injection", 0)),
            threshold=self.settings.threshold,
        )
