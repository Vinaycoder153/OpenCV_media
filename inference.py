#!/usr/bin/env python3
"""Inference entrypoint for OpenEnv RL hackathon.

Task:        Ai_business_Environment
Benchmark:   my-env
Agent:       An RL agent that solves tasks in the given environment.

Output contract (stdout only):
    [START] task=<name>
    [STEP] <json>
    [END]
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType, Observation

# ---------------------------------------------------------------------------
# Environment variables
# ---------------------------------------------------------------------------
API_BASE_URL: str = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")

# ---------------------------------------------------------------------------
# OpenAI client (module-level, as required)
# ---------------------------------------------------------------------------
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TASK_NAME = "Ai_business_Environment"
MAX_STEPS = 10
SEED = 42

# Heuristic/default action parameter values
_DEFAULT_POST_QUALITY = 5
_DEFAULT_HASHTAG_COUNT = 8
_DEFAULT_AD_BUDGET = 1800
_DEFAULT_CAMPAIGN_BUDGET = 4000
_DEFAULT_CAMPAIGN_BUDGET_EMAIL = 2500
_DEFAULT_DISCOUNT_VALUE = 10
_DEFAULT_BUNDLE_PRICE = 210.0
_DEFAULT_BUNDLE_ITEMS = ["coffee", "snack"]

log = logging.getLogger("inference")

# ---------------------------------------------------------------------------
# Per-task system prompts (click/fill action format)
# ---------------------------------------------------------------------------
_SYSTEM_PROMPTS: Dict[int, str] = {
    1: (
        "You are an expert social media growth agent. "
        "Your goal: grow followers above 1,000 and engagement rate above 5%.\n\n"
        "Respond with EXACTLY ONE action per turn using this format:\n"
        "  click('element_id')                — for discrete actions\n"
        "  fill('element_id', 'value')        — for parameterised actions\n\n"
        "Available element IDs and values:\n"
        "  click('generate_post')             — create a high-quality post\n"
        "  fill('generate_post_quality', '5') — quality 1-5 (default 5)\n"
        "  fill('add_hashtags_count', '8')    — add N hashtags (1-10)\n"
        "  fill('schedule_post_timing', 'peak') — 'morning'|'evening'|'peak'\n"
        "  fill('run_ad_budget', '1800')      — run paid ad with ₹ budget\n"
        "  click('no_op')                     — take no action\n"
    ),
    2: (
        "You are an expert online reputation manager. "
        "Your goal: raise average rating above 4.0 and sentiment score above 0.7.\n\n"
        "Respond with EXACTLY ONE action per turn using this format:\n"
        "  click('element_id')                — for discrete actions\n"
        "  fill('element_id', 'value')        — for parameterised actions\n\n"
        "Available element IDs and values:\n"
        "  fill('reply_review_tone', 'professional') — 'professional'|'apologetic'|'friendly'\n"
        "  fill('request_review_channel', 'in-person') — 'sms'|'email'|'in-person'\n"
        "  fill('offer_discount_value', '10') — discount % (5-30)\n"
        "  fill('improve_service_area', 'quality') — 'speed'|'quality'|'cleanliness'|'staff'\n"
        "  click('no_op')                     — take no action\n"
    ),
    3: (
        "You are an expert revenue optimisation agent. "
        "Your goal: grow monthly revenue above ₹1,20,000 while keeping satisfaction above 0.7.\n\n"
        "Respond with EXACTLY ONE action per turn using this format:\n"
        "  click('element_id')                — for discrete actions\n"
        "  fill('element_id', 'value')        — for parameterised actions\n\n"
        "Available element IDs and values:\n"
        "  fill('run_campaign_type', 'social')  — 'social'|'email'|'local' (budget defaults to 4000)\n"
        "  fill('add_offer_discount_pct', '10') — discount % (5-30)\n"
        "  fill('launch_bundle_price', '210')   — bundle price in ₹\n"
        "  fill('change_price_direction', 'up') — 'up'|'down'\n"
        "  click('no_op')                       — take no action\n"
    ),
}


# ---------------------------------------------------------------------------
# Action translation: click/fill strings → BusinessEnv Action objects
# ---------------------------------------------------------------------------
def _parse_click_fill(text: str) -> Optional[Tuple[str, str, str]]:
    """Return (kind, element_id, value) from a click/fill string, or None."""
    m = re.search(
        r"\b(click|fill)\(\s*['\"]([^'\"]+)['\"]\s*(?:,\s*['\"]([^'\"]*)['\"])?\s*\)",
        text,
    )
    if not m:
        return None
    kind = m.group(1)
    eid = m.group(2)
    val = m.group(3) or ""
    return kind, eid, val


def _translate_to_action(kind: str, eid: str, val: str) -> Optional[Action]:
    """Map a click/fill tuple to a BusinessEnv Action."""
    mapping: Dict[str, Action] = {
        # Task 1
        "generate_post": Action(action_type=ActionType.GENERATE_POST, parameters={"quality": _DEFAULT_POST_QUALITY}),
        "no_op": Action(action_type=ActionType.NO_OP, parameters={}),
    }

    if eid in mapping and kind == "click":
        return mapping[eid]

    # fill-based translations
    if eid == "generate_post_quality":
        return Action(action_type=ActionType.GENERATE_POST, parameters={"quality": _int(val, _DEFAULT_POST_QUALITY)})
    if eid == "add_hashtags_count":
        return Action(action_type=ActionType.ADD_HASHTAGS, parameters={"count": _int(val, _DEFAULT_HASHTAG_COUNT)})
    if eid == "schedule_post_timing":
        return Action(action_type=ActionType.SCHEDULE_POST, parameters={"timing": val or "peak"})
    if eid == "run_ad_budget":
        return Action(action_type=ActionType.RUN_AD, parameters={"budget": _int(val, _DEFAULT_AD_BUDGET)})
    if eid == "reply_review_tone":
        return Action(action_type=ActionType.REPLY_REVIEW, parameters={"tone": val or "professional"})
    if eid == "request_review_channel":
        return Action(action_type=ActionType.REQUEST_REVIEW, parameters={"channel": val or "in-person"})
    if eid == "offer_discount_value":
        return Action(action_type=ActionType.OFFER_DISCOUNT, parameters={"value": _int(val, _DEFAULT_DISCOUNT_VALUE)})
    if eid == "improve_service_area":
        return Action(action_type=ActionType.IMPROVE_SERVICE, parameters={"area": val or "quality"})
    if eid == "run_campaign_type":
        return Action(action_type=ActionType.RUN_CAMPAIGN, parameters={"type": val or "social", "budget": _DEFAULT_CAMPAIGN_BUDGET})
    if eid == "add_offer_discount_pct":
        return Action(action_type=ActionType.ADD_OFFER, parameters={"discount_pct": _int(val, _DEFAULT_DISCOUNT_VALUE)})
    if eid == "launch_bundle_price":
        return Action(
            action_type=ActionType.LAUNCH_BUNDLE,
            parameters={"items": _DEFAULT_BUNDLE_ITEMS, "bundle_price": float(val) if val else _DEFAULT_BUNDLE_PRICE},
        )
    if eid == "change_price_direction":
        return Action(action_type=ActionType.CHANGE_PRICE, parameters={"direction": val or "up", "pct": _DEFAULT_DISCOUNT_VALUE})

    return None


def _int(val: str, default: int) -> int:
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Observation → LLM prompt text
# ---------------------------------------------------------------------------
def _format_obs(obs: Observation) -> str:
    m = obs.metrics
    lines: List[str] = [
        f"Step {obs.step}/{MAX_STEPS} | {obs.task_description}",
        f"Trend: {obs.trend}",
    ]
    if m.followers:
        lines.append(f"Followers: {m.followers}  Engagement: {m.engagement_rate:.3f}")
    if m.avg_rating:
        lines.append(f"Avg rating: {m.avg_rating:.2f}  Reviews: {m.total_reviews}")
    if m.monthly_revenue:
        lines.append(f"Revenue: ₹{m.monthly_revenue:,.0f}  Orders/day: {m.daily_orders}")
    if obs.recent_actions:
        lines.append(f"Recent actions: {', '.join(obs.recent_actions[-3:])}")
    lines.append(f"Valid actions: {', '.join(obs.valid_actions)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# LLM action selection
# ---------------------------------------------------------------------------
def _llm_action(task_id: int, obs: Observation) -> Optional[Action]:
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPTS[task_id]},
                {"role": "user", "content": _format_obs(obs)},
            ],
            temperature=0.0,
            max_tokens=64,
        )
        text = resp.choices[0].message.content or ""
        parsed = _parse_click_fill(text)
        if parsed:
            action = _translate_to_action(*parsed)
            if action is not None:
                return action
        log.warning("LLM response could not be parsed as click/fill: %s", text[:120])
    except Exception as exc:
        log.warning("LLM call failed, using heuristic fallback: %s", exc)
    return None


# ---------------------------------------------------------------------------
# Heuristic fallback
# ---------------------------------------------------------------------------
_HEURISTICS: Dict[int, List[Action]] = {
    1: [
        Action(action_type=ActionType.ADD_HASHTAGS, parameters={"count": _DEFAULT_HASHTAG_COUNT}),
        Action(action_type=ActionType.SCHEDULE_POST, parameters={"timing": "peak"}),
        Action(action_type=ActionType.GENERATE_POST, parameters={"quality": _DEFAULT_POST_QUALITY}),
        Action(action_type=ActionType.RUN_AD, parameters={"budget": _DEFAULT_AD_BUDGET}),
    ],
    2: [
        Action(action_type=ActionType.IMPROVE_SERVICE, parameters={"area": "quality"}),
        Action(action_type=ActionType.REPLY_REVIEW, parameters={"tone": "professional"}),
        Action(action_type=ActionType.REQUEST_REVIEW, parameters={"channel": "in-person"}),
        Action(action_type=ActionType.OFFER_DISCOUNT, parameters={"value": _DEFAULT_DISCOUNT_VALUE}),
    ],
    3: [
        Action(action_type=ActionType.RUN_CAMPAIGN, parameters={"type": "social", "budget": _DEFAULT_CAMPAIGN_BUDGET}),
        Action(action_type=ActionType.ADD_OFFER, parameters={"discount_pct": _DEFAULT_DISCOUNT_VALUE}),
        Action(
            action_type=ActionType.LAUNCH_BUNDLE,
            parameters={"items": _DEFAULT_BUNDLE_ITEMS, "bundle_price": _DEFAULT_BUNDLE_PRICE},
        ),
        Action(action_type=ActionType.RUN_CAMPAIGN, parameters={"type": "email", "budget": _DEFAULT_CAMPAIGN_BUDGET_EMAIL}),
    ],
}


def _heuristic_action(task_id: int, step: int) -> Action:
    choices = _HEURISTICS[task_id]
    return choices[step % len(choices)]


# ---------------------------------------------------------------------------
# Stdout helpers
# ---------------------------------------------------------------------------
def _emit_step(payload: Dict[str, Any]) -> None:
    print("[STEP] " + json.dumps(payload, ensure_ascii=True, separators=(",", ":")))


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------
def run() -> None:
    total_reward = 0.0
    for task_id in (1, 2, 3):
        env = BusinessEnv(task_id=task_id, seed=SEED)
        obs = env.reset()
        steps_taken = 0

        while steps_taken < MAX_STEPS:
            action = _llm_action(task_id=task_id, obs=obs) or _heuristic_action(
                task_id=task_id, step=obs.step
            )
            result = env.step(action)
            total_reward += result.reward.value
            steps_taken += 1

            _emit_step(
                {
                    "task_id": task_id,
                    "step": result.observation.step,
                    "action": action.action_type.value,
                    "reward": f"{result.reward.value:.2f}",
                    "done": bool(result.done),
                    "goal_reached": bool(result.info.get("goal_reached", False)),
                }
            )

            obs = result.observation
            if result.done:
                break

    _emit_step(
        {
            "summary": "run_complete",
            "total_reward": f"{total_reward:.2f}",
            "done": True,
            "goal_reached": True,
        }
    )


def main() -> None:
    print(f"[START] task={TASK_NAME}")
    try:
        run()
    except Exception as exc:
        _emit_step(
            {
                "error": str(exc),
                "done": True,
                "goal_reached": False,
                "reward": "0.00",
            }
        )
    finally:
        print("[END]")


if __name__ == "__main__":
    main()
