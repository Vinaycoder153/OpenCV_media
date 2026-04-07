#!/usr/bin/env python3
"""OpenAI API client helper with validation.

Provides a factory with pre-flight validation so the rest of the codebase
can standardize client construction for local, cloud, and Hugging Face setups.
"""

from __future__ import annotations

import logging
from typing import Optional

from openai import OpenAI

log = logging.getLogger(__name__)


def validate_api_key(api_key: str, provider: str = "openai") -> str:
    """Validate and return API key with clear error messages.

    Parameters
    ----------
    api_key:
        Token to validate.
    provider:
        Provider name for error messages.

    Returns
    -------
    str:
        The validated API key.

    Raises
    ------
    ValueError:
        If the API key is invalid.
    """
    if not api_key or not api_key.strip():
        raise ValueError(
            f"{provider.upper()}_API_KEY is required but empty or not set. "
            f"Set via environment variable or pass as function argument."
        )

    api_key = api_key.strip()

    # Basic format validation
    if provider == "openai" and not api_key.startswith("sk-"):
        log.warning(
            f"OpenAI key does not start with 'sk-'. "
            f"You may have the wrong API key format."
        )

    return api_key


def create_openai_client(
    api_key: str,
    base_url: Optional[str] = None,
    validate: bool = True,
) -> OpenAI:
    """Create and return an OpenAI client.

    Parameters
    ----------
    api_key:
        Token used for the OpenAI-compatible endpoint.
    base_url:
        Optional OpenAI-compatible API endpoint (default: OpenAI public).
    validate:
        Whether to pre-validate the API key (default: True).

    Returns
    -------
    OpenAI:
        Configured client ready for use.

    Raises
    ------
    ValueError:
        If api_key is invalid or empty.
    """
    if validate:
        api_key = validate_api_key(api_key, provider="openai")

    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)
