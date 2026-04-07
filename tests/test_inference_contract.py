from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INFERENCE_PATH = REPO_ROOT / "inference.py"


def _run_inference(
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "USE_LLM": "false",
            "SEED": "42",
            "PYTHONPATH": str(REPO_ROOT),
        }
    )
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(INFERENCE_PATH)],
        cwd=str(REPO_ROOT),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _extract_step_payloads(stdout: str) -> list[dict]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    payloads: list[dict] = []
    for i, line in enumerate(lines):
        if line == "[STEP]" and i + 1 < len(lines):
            payloads.append(json.loads(lines[i + 1]))
    return payloads


def test_inference_emits_required_envelope() -> None:
    result = _run_inference()
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    assert lines[0] == "[START]"
    assert lines[-1] == "[END]"
    assert "[STEP]" in lines


def test_inference_step_payload_contract() -> None:
    result = _run_inference()
    payloads = _extract_step_payloads(result.stdout)

    assert payloads, "Expected at least one [STEP] payload"

    for payload in payloads:
        if "reward" in payload:
            reward = payload["reward"]
            assert isinstance(reward, str)
            assert reward.count(".") == 1
            decimals = reward.split(".")[1]
            assert len(decimals) == 2

        for flag in ("done", "goal_reached"):
            if flag in payload:
                assert isinstance(payload[flag], bool)


def test_inference_llm_mode_without_token_still_emits_end() -> None:
    result = _run_inference({"USE_LLM": "true", "HF_TOKEN": ""})
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    payloads = _extract_step_payloads(result.stdout)

    assert lines[0] == "[START]"
    assert lines[-1] == "[END]"
    assert payloads
    assert "error" in payloads[-1]
    assert payloads[-1].get("done") is True
