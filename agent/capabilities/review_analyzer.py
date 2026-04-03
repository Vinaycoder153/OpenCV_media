"""Customer review analyser capability."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import REVIEW_ANALYSIS_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def analyze_reviews(
    agent: "BusinessGrowthAgent",
    business_type: str,
    location: str,
    reviews: Union[List[str], str],
) -> str:
    """
    Analyse customer reviews for sentiment, insights, and improvement areas.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    business_type:
        Type of business.
    location:
        Business location.
    reviews:
        Either a list of review strings or a single block of text containing
        multiple reviews separated by newlines.

    Returns
    -------
    str
        Sentiment breakdown, key themes, actionable improvements, and a
        sample owner-response template.
    """
    if isinstance(reviews, list):
        reviews_text = "\n".join(
            f"{i + 1}. {r.strip()}" for i, r in enumerate(reviews) if r.strip()
        )
    else:
        reviews_text = reviews.strip()

    if not reviews_text:
        return "⚠️ No reviews provided. Please supply at least one review to analyse."

    context = build_business_context(
        business_type=business_type,
        location=location,
        focus_area="review recovery",
        problem="improve rating and sentiment",
    )
    prompt = REVIEW_ANALYSIS_PROMPT.format(
        business_type=business_type,
        location=location,
        reviews=reviews_text,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
