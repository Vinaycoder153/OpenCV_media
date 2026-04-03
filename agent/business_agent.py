"""
Core Business Growth Agent class.

Orchestrates all seven capabilities and manages conversation history so that
the agent can be used both as a single-turn advisor and as a multi-turn
interactive assistant.
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict, List, Optional, Union

from agent.gemini_client import create_gemini_client
from agent.intelligence import build_fallback_response
from agent.prompts import SYSTEM_PROMPT
from agent.capabilities.social_media import generate_social_media_content
from agent.capabilities.growth_strategy import suggest_growth_strategy
from agent.capabilities.review_analyzer import analyze_reviews
from agent.capabilities.performance_report import generate_performance_report
from agent.capabilities.persona_generator import generate_customer_personas
from agent.capabilities.pricing_advisor import suggest_pricing_and_offers
from agent.capabilities.action_planner import create_daily_action_plan
from agent.capabilities.instagram_content import generate_instagram_content
from agent.capabilities.problem_solver import solve_business_problem


class BusinessGrowthAgent:
    """
    AI Business Growth Partner for small and local Indian businesses.

    Wraps a Google Gemini chat-completion client and exposes all nine capabilities
    as friendly, type-annotated methods.

    Parameters
    ----------
    api_key:
        Google API key.  Falls back to the ``GOOGLE_API_KEY`` environment
        variable when not supplied.
    model:
        Gemini model to use (default: ``"gemini-1.5-flash"``).
    temperature:
        Sampling temperature (0.0 – 2.0).  Lower values produce more
        consistent, structured output; higher values add creativity.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "Google API key is required.  Pass it as `api_key` or set the "
                "GOOGLE_API_KEY environment variable."
            )
        self._logger = logging.getLogger(__name__)
        self._client = create_gemini_client(api_key=resolved_key)
        self.model = model or os.environ.get("GOOGLE_MODEL", "gemini-1.5-flash")
        temp_from_env = os.environ.get("GOOGLE_TEMPERATURE")
        self.temperature = (
            temperature
            if temperature is not None
            else self._parse_temperature(temp_from_env)
        )
        self._history: List[Dict[str, str]] = []

    # ------------------------------------------------------------------
    # Low-level chat helper
    # ------------------------------------------------------------------

    def chat(self, user_message: str, *, reset_history: bool = False) -> str:
        """
        Send a message to the LLM and return the response text.

        The agent keeps a rolling conversation history so follow-up questions
        maintain context.  Call with ``reset_history=True`` to start a fresh
        conversation.

        Parameters
        ----------
        user_message:
            The prompt / question to send.
        reset_history:
            When ``True``, clears previous conversation turns before sending.

        Returns
        -------
        str
            The assistant's response.
        """
        if reset_history:
            self._history = []

        self._history.append({"role": "user", "content": user_message})

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self._history,
        ]

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            reply = response.choices[0].message.content or ""
        except Exception as exc:
            self._logger.warning("LLM request failed: %s", exc)
            reply = build_fallback_response(user_message)
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def chat_with_context(
        self, user_message: str, context: str, *, reset_history: bool = False
    ) -> str:
        """Send a message with an explicit business context block."""
        composed = (
            f"{context}\n\nUser request:\n{user_message}" if context else user_message
        )
        return self.chat(composed, reset_history=reset_history)

    def _parse_temperature(self, value: Optional[str]) -> float:
        try:
            if value is None or value.strip() == "":
                return 0.7
            return max(0.0, min(2.0, float(value)))
        except Exception:
            return 0.7

    def reset_history(self) -> None:
        """Clear the current conversation history."""
        self._history = []

    # ------------------------------------------------------------------
    # Capability 1 – Social media content
    # ------------------------------------------------------------------

    def social_media_content(
        self,
        business_type: str,
        location: str,
        target_audience: str,
        platform: str = "Instagram",
        theme: str = "general promotion",
        tone: str = "friendly and engaging",
        num_posts: int = 3,
    ) -> str:
        """Generate platform-optimised social media posts with hashtags and tips."""
        return generate_social_media_content(
            self,
            business_type=business_type,
            location=location,
            target_audience=target_audience,
            platform=platform,
            theme=theme,
            tone=tone,
            num_posts=num_posts,
        )

    # ------------------------------------------------------------------
    # Capability 2 – Growth strategy
    # ------------------------------------------------------------------

    def growth_strategy(
        self,
        business_type: str,
        location: str,
        problem: str,
        monthly_revenue: int = 0,
        marketing_budget: int = 0,
    ) -> str:
        """Provide a targeted growth strategy to solve a specific business challenge."""
        return suggest_growth_strategy(
            self,
            business_type=business_type,
            location=location,
            problem=problem,
            monthly_revenue=monthly_revenue,
            marketing_budget=marketing_budget,
        )

    # ------------------------------------------------------------------
    # Capability 3 – Review analysis
    # ------------------------------------------------------------------

    def analyze_reviews(
        self,
        business_type: str,
        location: str,
        reviews: Union[List[str], str],
    ) -> str:
        """Analyse customer reviews for sentiment, key themes, and improvements."""
        return analyze_reviews(
            self,
            business_type=business_type,
            location=location,
            reviews=reviews,
        )

    # ------------------------------------------------------------------
    # Capability 4 – Performance report
    # ------------------------------------------------------------------

    def performance_report(
        self,
        business_type: str,
        location: str,
        footfall: int,
        revenue: int,
        new_customers: int,
        repeat_customers: int,
        top_item: str,
        social_reach: int = 0,
    ) -> str:
        """Generate a structured weekly performance report with goals."""
        return generate_performance_report(
            self,
            business_type=business_type,
            location=location,
            footfall=footfall,
            revenue=revenue,
            new_customers=new_customers,
            repeat_customers=repeat_customers,
            top_item=top_item,
            social_reach=social_reach,
        )

    # ------------------------------------------------------------------
    # Capability 5 – Customer personas
    # ------------------------------------------------------------------

    def customer_personas(
        self,
        business_type: str,
        location: str,
        avg_transaction: int,
        peak_hours: str,
        observations: str = "",
    ) -> str:
        """Generate detailed customer personas to guide targeting and retention."""
        return generate_customer_personas(
            self,
            business_type=business_type,
            location=location,
            avg_transaction=avg_transaction,
            peak_hours=peak_hours,
            observations=observations,
        )

    # ------------------------------------------------------------------
    # Capability 6 – Pricing & offers
    # ------------------------------------------------------------------

    def pricing_and_offers(
        self,
        business_type: str,
        location: str,
        current_pricing: str,
        goal: str,
        competitor_pricing: str = "unknown",
    ) -> str:
        """Suggest pricing strategies, bundles, and loyalty programmes."""
        return suggest_pricing_and_offers(
            self,
            business_type=business_type,
            location=location,
            current_pricing=current_pricing,
            goal=goal,
            competitor_pricing=competitor_pricing,
        )

    # ------------------------------------------------------------------
    # Capability 7 – Instagram content kit
    # ------------------------------------------------------------------

    def instagram_content(
        self,
        business_type: str,
        location: str,
        audience: str,
    ) -> str:
        """Generate an Instagram post, caption, 10 hashtags, and a Reel idea."""
        return generate_instagram_content(
            self,
            business_type=business_type,
            location=location,
            audience=audience,
        )

    # ------------------------------------------------------------------
    # Capability 8 – Daily action plan
    # ------------------------------------------------------------------

    def daily_action_plan(
        self,
        business_type: str,
        location: str,
        focus_area: str,
        available_time: float = 8.0,
        budget: int = 0,
    ) -> str:
        """Create a practical, time-boxed daily action plan for the owner."""
        return create_daily_action_plan(
            self,
            business_type=business_type,
            location=location,
            focus_area=focus_area,
            available_time=available_time,
            budget=budget,
        )

    # ------------------------------------------------------------------
    # Capability 9 – Business problem solver
    # ------------------------------------------------------------------

    def solve_business_problem(
        self,
        problem: str,
        details: str,
    ) -> str:
        """Generate low-budget, high-impact solutions for a specific business problem."""
        return solve_business_problem(
            self,
            problem=problem,
            details=details,
        )
