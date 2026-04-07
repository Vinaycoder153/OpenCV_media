#!/usr/bin/env python3
"""Pre-flight environment validation for hackathon submission.

Checks all required variables, formats, and defaults before running inference.
"""

from __future__ import annotations

import os
import sys
import logging
from typing import Dict, List, Tuple

logging.basicConfig(
    format="%(levelname)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


def check_environment() -> Tuple[bool, List[str]]:
    """Validate entire environment configuration.

    Returns
    -------
    (is_valid, warnings)
        is_valid: True if all critical checks pass
        warnings: List of warning messages
    """
    warnings: List[str] = []
    critical_errors: List[str] = []

    # Check 1: Hackathon defaults are set correctly
    api_base_url = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
    if api_base_url != "https://api.openai.com/v1":
        warnings.append(
            f"API_BASE_URL is non-standard: {api_base_url}. "
            f"Expected: https://api.openai.com/v1"
        )

    model_name = os.environ.get("MODEL_NAME", "gpt-4o-mini")
    if model_name != "gpt-4o-mini":
        warnings.append(
            f"MODEL_NAME is non-standard: {model_name}. " f"Expected: gpt-4o-mini"
        )

    # Check 2: If USE_LLM=true, validate HF_TOKEN
    use_llm = os.environ.get("USE_LLM", "false").lower() in {"1", "true", "yes"}
    if use_llm:
        hf_token = os.environ.get("HF_TOKEN", "").strip()
        if not hf_token:
            critical_errors.append(
                "USE_LLM=true but HF_TOKEN is empty. "
                "Set HF_TOKEN before running inference."
            )

    # Check 3: SEED is properly set for determinism
    try:
        seed = int(os.environ.get("SEED", "42"))
        if seed != 42:
            warnings.append(f"SEED is {seed}, expected 42 for reproducibility.")
    except ValueError:
        critical_errors.append(f"SEED is not an integer: {os.environ.get('SEED')}")

    # Check 4: Temperature is reasonable
    try:
        temp = float(os.environ.get("MODEL_TEMPERATURE", "0.0"))
        if temp != 0.0:
            warnings.append(
                f"MODEL_TEMPERATURE is {temp}, expected 0.0 for determinism."
            )
    except ValueError:
        critical_errors.append(
            f"MODEL_TEMPERATURE is not a float: {os.environ.get('MODEL_TEMPERATURE')}"
        )

    # Check 5: OpenAI API key not exposed
    if "sk-" in sys.argv.__str__():
        warnings.append(
            "OpenAI API key appears in command line. Use environment variable instead."
        )

    # Print results
    if critical_errors:
        log.error("CRITICAL ERRORS found:")
        for err in critical_errors:
            log.error(f"  ❌ {err}")
        return False, warnings

    if warnings:
        log.warning("WARNINGS (non-critical):")
        for warn in warnings:
            log.warning(f"  ⚠️  {warn}")

    log.info("✅ Environment validation PASSED")
    return True, warnings


if __name__ == "__main__":
    is_valid, warnings = check_environment()
    sys.exit(0 if is_valid else 1)
