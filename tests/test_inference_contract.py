#!/usr/bin/env python3
"""Contract tests for inference.py output format compliance.

Validates that inference produces properly formatted output per hackathon spec.
"""

from __future__ import annotations

import json
import subprocess
import sys
import os
from typing import Optional


def run_inference() -> str:
    """Run inference.py and capture output.

    Returns
    -------
    str
        Raw stdout from inference.py
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    result = subprocess.run(
        [sys.executable, os.path.join(repo_root, "inference.py")],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=repo_root,
    )
    return result.stdout + result.stderr


def parse_steps(output: str) -> list:
    """Parse [STEP] entries from output.

    Parameters
    ----------
    output : str
        Raw output from inference.py

    Returns
    -------
    list
        List of parsed JSON payloads
    """
    steps = []
    lines = output.split("\n")

    i = 0
    while i < len(lines):
        if lines[i].strip() == "[STEP]":
            if i + 1 < len(lines):
                try:
                    payload = json.loads(lines[i + 1])
                    steps.append(payload)
                    i += 2
                except json.JSONDecodeError:
                    i += 1
        else:
            i += 1

    return steps


def test_output_envelope():
    """Test that output has correct START/END markers."""
    output = run_inference()
    lines = [l for l in output.strip().split("\n") if l.strip()]

    assert "[START]" in lines[0], f"First line should contain [START], got {lines[0]}"
    assert "[END]" in lines[-1], f"Last line should contain [END], got {lines[-1]}"

    print("✅ Output envelope correct (START/END)")


def test_step_format():
    """Test that [STEP] entries are valid JSON."""
    output = run_inference()
    steps = parse_steps(output)

    assert len(steps) > 0, "No [STEP] entries found in output"

    for i, step in enumerate(steps):
        assert isinstance(step, dict), f"Step {i} not a JSON object"

        if "action" in step:
            assert "reward" in step, f"Step {i} has action but no reward"
            assert isinstance(step["reward"], str), f"Reward should be string"
            try:
                reward_val = float(step["reward"])
                assert (
                    step["reward"] == f"{reward_val:.2f}"
                ), f"Reward not 2 decimals: {step['reward']}"
            except ValueError:
                raise AssertionError(f"Reward is not numeric: {step['reward']}")

    print(f"✅ Step format valid ({len(steps)} steps)")


def test_json_booleans():
    """Test that booleans are lowercase JSON."""
    output = run_inference()

    assert " True" not in output, "Python-style True found"
    assert " False" not in output, "Python-style False found"

    steps = parse_steps(output)
    for step in steps:
        if "done" in step:
            assert step["done"] in [
                True,
                False,
                "true",
                "false",
            ], f"Boolean format error: {step['done']}"

    print("✅ Booleans are lowercase JSON")


def test_determinism():
    """Test that running twice produces same result."""
    output1 = run_inference()
    output2 = run_inference()

    steps1 = parse_steps(output1)
    steps2 = parse_steps(output2)

    assert len(steps1) == len(
        steps2
    ), f"Step count differs: {len(steps1)} vs {len(steps2)}"

    for i, (s1, s2) in enumerate(zip(steps1, steps2)):
        assert s1.get("action") == s2.get(
            "action"
        ), f"Action differs at step {i}: {s1.get('action')} vs {s2.get('action')}"

    print("✅ Determinism verified")


def test_no_api_calls_when_llm_false():
    """Test that no API calls made when USE_LLM=false."""
    env = os.environ.copy()
    env["USE_LLM"] = "false"
    env["OPENAI_API_KEY"] = ""

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        [sys.executable, os.path.join(repo_root, "inference.py")],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=repo_root,
        env=env,
    )

    assert "OPENAI_API_KEY is required" not in result.stderr
    assert "[END]" in result.stdout

    print("✅ No API key required for heuristic baseline")


if __name__ == "__main__":
    tests = [
        test_output_envelope,
        test_step_format,
        test_json_booleans,
        test_determinism,
        test_no_api_calls_when_llm_false,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            print(f"\nRunning {test.__name__}...")
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    sys.exit(0 if failed == 0 else 1)
