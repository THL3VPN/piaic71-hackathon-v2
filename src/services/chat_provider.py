from __future__ import annotations

import os
from dataclasses import dataclass

# [Task]: T003 [From]: specs/012-ai-agent-integration/spec.md User Story 2
# [Task]: T015 [From]: specs/012-ai-agent-integration/spec.md User Story 2


@dataclass(frozen=True)
class ChatProviderSettings:
    provider: str | None
    model_name: str | None
    history_limit: int
    openai_api_key: str | None
    gemini_api_key: str | None


class ProviderConfigError(ValueError):
    """Raised when provider configuration is invalid."""


def _read_int(value: str | None, default: int) -> int:
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def validate_provider_settings(settings: ChatProviderSettings) -> ChatProviderSettings:
    provider = (settings.provider or "").strip().lower()
    if not provider:
        raise ProviderConfigError("CHAT_MODEL_PROVIDER is required")
    if provider not in {"openai", "gemini"}:
        raise ProviderConfigError("CHAT_MODEL_PROVIDER must be 'openai' or 'gemini'")

    model_name = (settings.model_name or "").strip()
    if not model_name:
        raise ProviderConfigError("CHAT_MODEL_NAME is required")

    if provider == "openai" and not settings.openai_api_key:
        raise ProviderConfigError("OPENAI_API_KEY is required")
    if provider == "gemini" and not settings.gemini_api_key:
        raise ProviderConfigError("GEMINI_API_KEY is required")

    return ChatProviderSettings(
        provider=provider,
        model_name=model_name,
        history_limit=settings.history_limit,
        openai_api_key=settings.openai_api_key,
        gemini_api_key=settings.gemini_api_key,
    )


def load_provider_settings(env: dict[str, str] | None = None) -> ChatProviderSettings:
    env = env or os.environ
    return ChatProviderSettings(
        provider=env.get("CHAT_MODEL_PROVIDER"),
        model_name=env.get("CHAT_MODEL_NAME"),
        history_limit=_read_int(env.get("CHAT_HISTORY_LIMIT"), 50),
        openai_api_key=env.get("OPENAI_API_KEY"),
        gemini_api_key=env.get("GEMINI_API_KEY"),
    )
