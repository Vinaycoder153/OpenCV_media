#!/usr/bin/env python3
"""OpenAI API client helper.

Provides a tiny factory so the rest of the codebase can standardize client
construction and base URL handling for local, cloud, and Hugging Face setups.
"""

from __future__ import annotations

from typing import Optional

from openai import OpenAI


def create_openai_client(api_key: str, base_url: Optional[str] = None) -> OpenAI:
    """Create and return an OpenAI client.

    Parameters
    ----------
    api_key:
        Token used for the OpenAI-compatible endpoint.
    base_url:
        Optional OpenAI-compatible API endpoint.
    """
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)
