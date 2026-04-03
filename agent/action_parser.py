"""Action parsing utilities: LLM text ↔ Action objects."""

from __future__ import annotations

import json
import re
from typing import Dict, Optional

from env.models.schemas import Action, ActionType

# Per-task system prompts for the baseline LLM agent
TASK_ACTION_PROMPTS: Dict[int, str] = {
    1: (
        "You are an expert social media growth consultant for small Indian businesses. "
        "Your goal is to grow followers above 1 000 and engagement rate above 5%. "
        "Choose ONE action per step. Respond ONLY with a JSON object, e.g.:\n"
        '{"action_type": "generate_post", "parameters": {"quality": 4}}\n\n'
        "Available actions:\n"
        "  generate_post      — quality: int 1-5\n"
        "  add_hashtags       — count: int 1-10\n"
        "  schedule_post      — timing: 'morning'|'evening'|'peak'\n"
        "  run_ad             — budget: int (₹)\n"
        "  no_op              — no parameters\n"
    ),
    2: (
        "You are an expert online reputation manager for small Indian businesses. "
        "Your goal is to raise the average rating above 4.0 and sentiment score above 0.7. "
        "Choose ONE action per step. Respond ONLY with a JSON object, e.g.:\n"
        '{"action_type": "reply_review", "parameters": {"tone": "professional"}}\n\n'
        "Available actions:\n"
        "  reply_review       — tone: 'professional'|'apologetic'|'friendly'\n"
        "  request_review     — channel: 'sms'|'email'|'in-person'\n"
        "  offer_discount     — value: int % (5-30)\n"
        "  improve_service    — area: 'speed'|'quality'|'cleanliness'|'staff'\n"
        "  no_op              — no parameters\n"
    ),
    3: (
        "You are an expert revenue optimization consultant for small Indian businesses. "
        "Your goal is to grow monthly revenue above ₹1,20,000 while keeping "
        "customer satisfaction above 0.7. "
        "Choose ONE action per step. Respond ONLY with a JSON object, e.g.:\n"
        '{"action_type": "run_campaign", "parameters": {"type": "social", "budget": 5000}}\n\n'
        "Available actions:\n"
        "  change_price       — direction: 'up'|'down', pct: int %\n"
        "  add_offer          — discount_pct: int % (5-30)\n"
        "  run_campaign       — type: 'social'|'email'|'local', budget: int (₹)\n"
        "  launch_bundle      — items: list[str], bundle_price: float\n"
        "  no_op              — no parameters\n"
    ),
}


def parse_action_from_text(text: str) -> Optional[Action]:
    """Parse a JSON action from raw LLM output.

    Tries to extract a JSON object from the text even if there is surrounding
    prose. Returns ``None`` if parsing fails.
    """
    # Try direct parse first
    stripped = text.strip()
    try:
        data = json.loads(stripped)
        return Action(
            action_type=ActionType(data["action_type"]),
            parameters=data.get("parameters", {}),
        )
    except Exception:
        pass

    # Try to find a JSON block inside the text
    match = re.search(r"\{.*?\}", stripped, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return Action(
                action_type=ActionType(data["action_type"]),
                parameters=data.get("parameters", {}),
            )
        except Exception:
            pass

    return None


def action_to_prompt_description(action: Action) -> str:
    """Return a human-readable description of an action."""
    params = ", ".join(f"{k}={v}" for k, v in action.parameters.items())
    if params:
        return f"{action.action_type.value}({params})"
    return action.action_type.value


def format_observation_for_llm(obs) -> str:  # obs: Observation
    """Format an Observation as a readable string for the LLM prompt."""
    m = obs.metrics
    lines = [
        f"Step {obs.step} | Task {obs.task_id}: {obs.task_description}",
        f"Trend: {obs.trend}",
        "Metrics:",
    ]
    if m.followers:
        lines.append(f"  followers={m.followers}  engagement_rate={m.engagement_rate:.3f}")
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
