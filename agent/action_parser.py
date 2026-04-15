"""Action parsing utilities: LLM text ↔ Action objects.

Type-safe, deterministic action parsing with graceful fallback.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Dict, Optional

from env.models.schemas import Action, ActionType

log = logging.getLogger(__name__)

# Per-task system prompts for LLM agent
TASK_ACTION_PROMPTS: Dict[int, str] = {
    1: (
        "You are an expert social media growth consultant for small Indian businesses. "
        "Your goal is to grow followers above 1,000 and engagement rate above 5%. "
        "Choose ONE action per step. Respond ONLY with a JSON object.\n\n"
        "STRATEGY: First boost hashtag quality (add_hashtags count=10), "
        "then create a high-quality post (generate_post quality=5), "
        "then run a paid ad (run_ad budget=3000+). Do NOT repeat the same "
        "action twice in a row — alternate to avoid spam penalties.\n\n"
        "Available actions:\n"
        '  generate_post      — quality: int 1-5  (e.g. {"action_type":"generate_post","parameters":{"quality":5}})\n'
        '  add_hashtags       — count: int 1-10   (e.g. {"action_type":"add_hashtags","parameters":{"count":10}})\n'
        '  schedule_post      — timing: "morning"|"evening"|"peak"\n'
        '  run_ad             — budget: int (₹)   (e.g. {"action_type":"run_ad","parameters":{"budget":3000}})\n'
        "  no_op              — no parameters\n"
    ),
    2: (
        "You are an expert online reputation manager for small Indian businesses. "
        "Your goal is to raise the average rating above 4.0 and sentiment score above 0.7. "
        "Choose ONE action per step. Respond ONLY with a JSON object.\n\n"
        "STRATEGY: Start with ONE request_review (in-person) to seed positive reviews, "
        "then strictly alternate between improve_service (area='quality') and "
        "reply_review (tone='professional'). This avoids diminishing returns "
        "(which penalise consecutive same-action-type uses). "
        "AVOID offer_discount and further request_review — they overwrite "
        "sentiment_score with the raw positive/total ratio which is much lower.\n\n"
        "Available actions:\n"
        '  reply_review       — tone: "professional"|"apologetic"|"friendly"\n'
        '  request_review     — channel: "sms"|"email"|"in-person"\n'
        "  offer_discount     — value: int % (5-30)\n"
        '  improve_service    — area: "speed"|"quality"|"cleanliness"|"staff"\n'
        "  no_op              — no parameters\n"
    ),
    3: (
        "You are an expert revenue optimization consultant for small Indian businesses. "
        "Your goal is to grow monthly revenue above ₹1,20,000 while keeping "
        "customer satisfaction above 0.7. "
        "Choose ONE action per step. Respond ONLY with a JSON object.\n\n"
        "STRATEGY: First use repeated add_offer (discount_pct=5) to raise "
        "customer_satisfaction toward 1.0 (each call adds +0.04). Once satisfaction "
        "is near 1.0, use launch_bundle with 5 items and a high bundle_price "
        "(e.g. 500) to massively boost AOV, orders, and revenue in one step. "
        "AVOID change_price (up) as it harms satisfaction. AVOID run_campaign "
        "before satisfaction is high enough.\n\n"
        "Available actions:\n"
        '  change_price       — direction: "up"|"down", pct: int %\n'
        "  add_offer          — discount_pct: int % (5-30)\n"
        '  run_campaign       — type: "social"|"email"|"local", budget: int (₹)\n'
        "  launch_bundle      — items: list[str], bundle_price: float\n"
        "  no_op              — no parameters\n"
    ),
}


def parse_action_from_text(text: str) -> Optional[Action]:
    """Parse a JSON action from raw LLM output.

    Tries to extract a JSON object from the text even if surrounded
    by prose. Returns ``None`` if parsing fails.

    Parameters
    ----------
    text : str
        Raw LLM response text.

    Returns
    -------
    Optional[Action]
        Parsed Action if successful, None otherwise.
    """
    if not text or not text.strip():
        log.debug("Empty text provided to parse_action_from_text")
        return None

    stripped: str = text.strip()

    # Try direct parse first
    try:
        data: Dict = json.loads(stripped)
        return Action(
            action_type=ActionType(data["action_type"]),
            parameters=data.get("parameters", {}),
        )
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        log.debug(f"Direct JSON parse failed: {e}")

    # Try to find a JSON block inside the text
    match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", stripped, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return Action(
                action_type=ActionType(data["action_type"]),
                parameters=data.get("parameters", {}),
            )
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            log.debug(f"Extracted JSON parse failed: {e}")

    log.warning(f"Could not parse action from text: {text[:100]}...")
    return None


def action_to_prompt_description(action: Action) -> str:
    """Return a human-readable description of an action.

    Parameters
    ----------
    action : Action
        The action to describe.

    Returns
    -------
    str
        Human-readable description.
    """
    params: str = ", ".join(f"{k}={v}" for k, v in action.parameters.items())
    if params:
        return f"{action.action_type.value}({params})"
    return action.action_type.value


def format_observation_for_llm(obs) -> str:
    """Format an Observation as a readable string for the LLM prompt.

    Parameters
    ----------
    obs : Observation
        The observation to format.

    Returns
    -------
    str
        Formatted observation text suitable for LLM input.
    """
    m = obs.metrics
    lines: list = [
        f"Step {obs.step} | Task {obs.task_id}: {obs.task_description}",
        f"Trend: {obs.trend}",
        "Metrics:",
    ]

    if m.followers > 0:
        lines.append(f"  Followers: {m.followers}, Engagement: {m.engagement_rate:.2f}")
    if m.avg_rating > 0:
        lines.append(f"  Rating: {m.avg_rating:.2f}, Reviews: {m.total_reviews}")
    if m.monthly_revenue > 0:
        lines.append(
            f"  Revenue: ₹{m.monthly_revenue:.0f}, Daily Orders: {m.daily_orders}"
        )

    lines.append(f"Recent actions: {', '.join(obs.recent_actions[-3:]) or 'none'}")
    lines.append(f"Valid actions: {', '.join(obs.valid_actions)}")
    if m.followers:
        lines.append(
            f"  followers={m.followers}  engagement_rate={m.engagement_rate:.3f}"
        )
    if m.avg_rating:
        lines.append(
            f"  avg_rating={m.avg_rating:.2f}  total_reviews={m.total_reviews}"
            f"  sentiment (see state)"
        )
    if m.monthly_revenue:
        lines.append(
            f"  monthly_revenue=₹{m.monthly_revenue:,.0f}"
            f"  daily_orders={m.daily_orders}"
            f"  avg_order_value=₹{m.avg_order_value:.0f}"
        )
    if obs.recent_actions:
        lines.append(f"Recent actions: {', '.join(obs.recent_actions)}")
    lines.append(f"Valid actions: {', '.join(obs.valid_actions)}")
    return "\n".join(lines)
