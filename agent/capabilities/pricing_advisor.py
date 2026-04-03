"""Pricing and offers advisor capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import PRICING_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def suggest_pricing_and_offers(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    current_pricing: str,
    goal: str,
    competitor_pricing: str = "unknown",
) -> str:
    """
    Suggest pricing strategies, bundle offers, and loyalty programmes.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        Type of business.
    location:
        Business location.
    current_pricing:
        Brief description of current pricing, e.g. "cappuccino ₹120, sandwich ₹90".
    goal:
        Pricing goal, e.g. "increase average order value" or "attract weekday customers".
    competitor_pricing:
        Competitor price reference if known.

    Returns
    -------
    str
        Structured pricing strategy with bundle ideas and a loyalty programme
        recommendation.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        focus_area="pricing optimization",
    )
    prompt = PRICING_PROMPT.format(
        business_type=business_type,
        location=location,
        current_pricing=current_pricing,
        competitor_pricing=competitor_pricing,
        goal=goal,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
