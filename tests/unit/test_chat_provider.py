from __future__ import annotations

import pytest

from src.services.chat_provider import (
    ChatProviderSettings,
    ProviderConfigError,
    validate_provider_settings,
)


# [Task]: T014 [From]: specs/012-ai-agent-integration/spec.md User Story 2


def _settings(**overrides: object) -> ChatProviderSettings:
    base = {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "history_limit": 50,
        "openai_api_key": "sk-test",
        "gemini_api_key": None,
    }
    base.update(overrides)
    return ChatProviderSettings(**base)


def test_validate_provider_settings_requires_provider() -> None:
    with pytest.raises(ProviderConfigError, match="CHAT_MODEL_PROVIDER"):
        validate_provider_settings(_settings(provider=None))


def test_validate_provider_settings_rejects_unknown_provider() -> None:
    with pytest.raises(ProviderConfigError, match="CHAT_MODEL_PROVIDER"):
        validate_provider_settings(_settings(provider="unknown"))


def test_validate_provider_settings_requires_model_name() -> None:
    with pytest.raises(ProviderConfigError, match="CHAT_MODEL_NAME"):
        validate_provider_settings(_settings(model_name=None))


def test_validate_provider_settings_requires_openai_key() -> None:
    with pytest.raises(ProviderConfigError, match="OPENAI_API_KEY"):
        validate_provider_settings(_settings(openai_api_key=None))


def test_validate_provider_settings_requires_gemini_key() -> None:
    settings = _settings(provider="gemini", gemini_api_key=None, openai_api_key=None)
    with pytest.raises(ProviderConfigError, match="GEMINI_API_KEY"):
        validate_provider_settings(settings)


def test_validate_provider_settings_accepts_valid_openai() -> None:
    settings = validate_provider_settings(_settings())
    assert settings.provider == "openai"

