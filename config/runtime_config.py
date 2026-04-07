"""Runtime configuration for hackathon inference entrypoint."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL_NAME = "gpt-4o-mini"
DEFAULT_SEED = 42


class RuntimeConfigError(ValueError):
    """Raised when required runtime config is missing or invalid."""


@dataclass(frozen=True)
class RuntimeConfig:
    api_base_url: str
    model_name: str
    seed: int
    use_llm: bool
    hf_token: str

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        api_base_url = os.environ.get("API_BASE_URL", DEFAULT_API_BASE_URL).strip()
        model_name = os.environ.get("MODEL_NAME", DEFAULT_MODEL_NAME).strip()
        use_llm = _parse_bool_env("USE_LLM", False)
        seed = _parse_int_env("SEED", DEFAULT_SEED)
        hf_token = os.environ.get("HF_TOKEN", "").strip()

        if not api_base_url:
            api_base_url = DEFAULT_API_BASE_URL
        if not model_name:
            model_name = DEFAULT_MODEL_NAME
        if use_llm and not hf_token:
            raise RuntimeConfigError(
                "HF_TOKEN is required when USE_LLM=true. Set HF_TOKEN or disable USE_LLM."
            )

        return cls(
            api_base_url=api_base_url,
            model_name=model_name,
            seed=seed,
            use_llm=use_llm,
            hf_token=hf_token,
        )


def _parse_bool_env(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _parse_int_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default
