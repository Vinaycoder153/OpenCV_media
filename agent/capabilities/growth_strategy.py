"""Growth strategy advisor capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import GROWTH_STRATEGY_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def suggest_growth_strategy(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    problem: str,
    monthly_revenue: int = 0,
    marketing_budget: int = 0,
) -> str:
    """
    Provide a targeted growth strategy to solve a specific business problem.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        E.g. "restaurant", "boutique".
    location:
        City or area.
    problem:
        The core business challenge, e.g. "footfall dropped 30% after a new
        competitor opened nearby".
    monthly_revenue:
        Approximate current monthly revenue in INR.
    marketing_budget:
        Available monthly marketing budget in INR.

    Returns
    -------
    str
        Structured growth strategy with prioritised action steps.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        problem=problem,
        revenue=monthly_revenue,
        budget=marketing_budget,
    )
    prompt = GROWTH_STRATEGY_PROMPT.format(
        business_type=business_type,
        location=location,
        monthly_revenue=monthly_revenue,
        problem=problem,
        marketing_budget=marketing_budget,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
