"""Social media content generator capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import SOCIAL_MEDIA_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def generate_social_media_content(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    target_audience: str,
    platform: str = "Instagram",
    theme: str = "general promotion",
    tone: str = "friendly and engaging",
    num_posts: int = 3,
) -> str:
    """
    Generate social media posts optimised for the given platform and business.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        E.g. "cafe", "salon", "restaurant".
    location:
        City or neighbourhood, e.g. "Koramangala, Bangalore".
    target_audience:
        Brief description, e.g. "college students aged 18-25".
    platform:
        Social platform (Instagram / Facebook / WhatsApp Status / YouTube Shorts).
    theme:
        Occasion or campaign theme, e.g. "Diwali offer", "weekend special".
    tone:
        Desired tone, e.g. "fun and casual", "professional", "festive".
    num_posts:
        Number of posts to generate (1-5).

    Returns
    -------
    str
        Formatted social media content with captions, hashtags, and tips.
    """
    num_posts = max(1, min(num_posts, 5))
    context = build_business_context(
        business_type=business_type,
        location=location,
        audience=target_audience,
        focus_area=f"{platform} growth",
        problem=theme,
    )
    prompt = SOCIAL_MEDIA_PROMPT.format(
        business_type=business_type,
        location=location,
        target_audience=target_audience,
        platform=platform,
        theme=theme,
        tone=tone,
        num_posts=num_posts,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
