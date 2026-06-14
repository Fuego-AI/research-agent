"""Configurações carregadas do arquivo .env (OpenRouter)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path, override=True)


def get_openrouter_api_key() -> str:
    """Chave de API para o OpenRouter."""
    return os.getenv("OPENROUTER_API_KEY", "").strip()


def get_openrouter_model_id() -> str:
    """ID do modelo no OpenRouter."""
    return os.getenv("OPENROUTER_MODEL_ID", "openai/gpt-oss-120b:free").strip()


def get_openrouter_base_url() -> str:
    """URL base da API do OpenRouter."""
    return "https://openrouter.ai/api/v1"


def get_gradio_server_port() -> int | None:
    port = os.getenv("GRADIO_SERVER_PORT")
    if port:
        return int(port)
    return None


def get_gradio_share() -> bool:
    return os.getenv("GRADIO_SHARE", "false").lower() in ("1", "true", "yes")
