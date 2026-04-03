"""Customer persona generator capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import PERSONA_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def generate_customer_personas(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    avg_transaction: int,
    peak_hours: str,
    observations: str = "",
) -> str:
    """
    Generate detailed customer personas to guide marketing and offers.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        Type of business.
    location:
        Business location.
    avg_transaction:
        Average spend per customer visit in INR.
    peak_hours:
        Busiest hours, e.g. "12 PM – 2 PM and 7 PM – 9 PM".
    observations:
        Any additional observations about customer behaviour.

    Returns
    -------
    str
        Two detailed customer personas with goals, pain points, and
        recommended retention strategies.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        focus_area="persona design",
    )
    prompt = PERSONA_PROMPT.format(
        business_type=business_type,
        location=location,
        avg_transaction=avg_transaction,
        peak_hours=peak_hours,
        observations=observations or "No additional observations",
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
