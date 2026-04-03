"""Instagram content generator capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import INSTAGRAM_CONTENT_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def generate_instagram_content(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    audience: str,
) -> str:
    """
    Generate a complete Instagram content kit for a local Indian business.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        E.g. "cafe", "salon", "boutique".
    location:
        City or neighbourhood, e.g. "Koramangala, Bangalore".
    audience:
        Brief description, e.g. "college students aged 18-25".

    Returns
    -------
    str
        Formatted output with an Instagram post, caption, 10 hashtags, and a
        Reel idea — all culturally tuned for India.
    """
    context = build_business_context(
        business_type=business_type,
        location=location,
        audience=audience,
        focus_area="instagram conversion",
    )
    prompt = INSTAGRAM_CONTENT_PROMPT.format(
        business_type=business_type,
        location=location,
        audience=audience,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
