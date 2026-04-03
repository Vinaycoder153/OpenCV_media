"""Daily action planner capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import ACTION_PLAN_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def create_daily_action_plan(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    focus_area: str,
    available_time: float = 8.0,
    budget: int = 0,
) -> str:
    """
    Create a practical, time-boxed daily action plan for the business owner.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        Type of business.
    location:
        Business location.
    focus_area:
        Today's primary focus, e.g. "social media growth", "improving service
        speed", "running a flash sale".
    available_time:
        Number of hours the owner can dedicate to growth tasks today.
    budget:
        Budget available for today's activities in INR.

    Returns
    -------
    str
        A structured day plan split into morning, business-hours, marketing,
        and wrap-up tasks plus a 30-day habit recommendation.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        focus_area=focus_area,
        budget=budget,
    )
    prompt = ACTION_PLAN_PROMPT.format(
        business_type=business_type,
        location=location,
        focus_area=focus_area,
        available_time=available_time,
        budget=budget,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
