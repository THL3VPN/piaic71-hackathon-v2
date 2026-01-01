from __future__ import annotations

from dataclasses import dataclass

from src.services.chat_provider import (
    ChatProviderSettings,
    ProviderConfigError,
    load_provider_settings,
    validate_provider_settings,
)

# [Task]: T004 [From]: specs/012-ai-agent-integration/spec.md User Story 2
# [Task]: T008 [From]: specs/012-ai-agent-integration/spec.md User Story 1
# [Task]: T016 [From]: specs/012-ai-agent-integration/spec.md User Story 2


class ModelFactoryError(RuntimeError):
    """Raised when model factory configuration is invalid."""


@dataclass(frozen=True)
class ChatModel:
    """Placeholder for provider-specific model object."""

    provider: str
    model_name: str
    client: object


def _require(value: str | None, label: str) -> str:
    if not value:
        raise ModelFactoryError(f"{label} is required")
    return value


def _build_openai(settings: ChatProviderSettings) -> ChatModel:
    api_key = _require(settings.openai_api_key, "OPENAI_API_KEY")
    model_name = _require(settings.model_name, "CHAT_MODEL_NAME")
    from openai import AsyncOpenAI  # type: ignore

    client = AsyncOpenAI(api_key=api_key)
    return ChatModel(provider="openai", model_name=model_name, client=client)


def _build_gemini(settings: ChatProviderSettings) -> ChatModel:
    api_key = _require(settings.gemini_api_key, "GEMINI_API_KEY")
    model_name = _require(settings.model_name, "CHAT_MODEL_NAME")
    from openai import AsyncOpenAI  # type: ignore

    client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    return ChatModel(provider="gemini", model_name=model_name, client=client)


def build_chat_model(settings: ChatProviderSettings | None = None) -> ChatModel:
    settings = settings or load_provider_settings()
    try:
        validated = validate_provider_settings(settings)
    except ProviderConfigError as exc:
        raise ModelFactoryError(str(exc)) from exc

    if validated.provider == "openai":
        return _build_openai(validated)
    if validated.provider == "gemini":
        return _build_gemini(validated)
    raise ModelFactoryError("CHAT_MODEL_PROVIDER must be 'openai' or 'gemini'")
