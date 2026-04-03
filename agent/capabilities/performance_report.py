"""Weekly performance report generator capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import PERFORMANCE_REPORT_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def generate_performance_report(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    footfall: int,
    revenue: int,
    new_customers: int,
    repeat_customers: int,
    top_item: str,
    social_reach: int = 0,
) -> str:
    """
    Generate a structured weekly performance report with insights and goals.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        Type of business.
    location:
        Business location.
    footfall:
        Total visitors / orders this week.
    revenue:
        Total revenue this week in INR.
    new_customers:
        Number of first-time customers.
    repeat_customers:
        Number of returning customers.
    top_item:
        Best-selling product or service this week.
    social_reach:
        Total social media reach / impressions (0 if not tracked).

    Returns
    -------
    str
        A formatted weekly report with wins, issues, trends, and goals.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        revenue=revenue,
        focus_area=f"weekly performance report for {top_item}",
    )
    prompt = PERFORMANCE_REPORT_PROMPT.format(
        business_type=business_type,
        location=location,
        footfall=footfall,
        revenue=revenue,
        new_customers=new_customers,
        repeat_customers=repeat_customers,
        top_item=top_item,
        social_reach=social_reach,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
