"""
Tests for the Business Growth Agent.

Uses unittest.mock to avoid real OpenAI API calls so the test suite can run
without an API key.
"""

from __future__ import annotations

import sys
import os
import types
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers to stub out the openai module before importing agent code
# ---------------------------------------------------------------------------

def _make_openai_stub() -> types.ModuleType:
    """Return a minimal fake `openai` module."""
    stub = types.ModuleType("openai")

    class FakeChoice:
        def __init__(self, content: str) -> None:
            self.message = MagicMock()
            self.message.content = content

    class FakeCompletion:
        def __init__(self, content: str) -> None:
            self.choices = [FakeChoice(content)]

    class FakeChat:
        def __init__(self) -> None:
            self.completions = MagicMock()
            self.completions.create = MagicMock(
                return_value=FakeCompletion("🚀 Quick Win\n- Fake response\n⚠️ Mistake to Avoid\n- Fake")
            )

    class FakeOpenAI:
        def __init__(self, api_key: str = "") -> None:
            self.chat = FakeChat()

    stub.OpenAI = FakeOpenAI
    return stub


# Inject the stub before importing anything from the agent package
sys.modules.setdefault("openai", _make_openai_stub())


# Now safe to import agent modules
from agent.business_agent import BusinessGrowthAgent  # noqa: E402
from agent.prompts import (  # noqa: E402
    SYSTEM_PROMPT,
    SOCIAL_MEDIA_PROMPT,
    GROWTH_STRATEGY_PROMPT,
    REVIEW_ANALYSIS_PROMPT,
    PERFORMANCE_REPORT_PROMPT,
    PERSONA_PROMPT,
    PRICING_PROMPT,
    ACTION_PLAN_PROMPT,
    INSTAGRAM_CONTENT_PROMPT,
    PROBLEM_SOLVER_PROMPT,
)


# ---------------------------------------------------------------------------
# BusinessGrowthAgent unit tests
# ---------------------------------------------------------------------------

class TestBusinessGrowthAgentInit(unittest.TestCase):
    def test_raises_without_api_key(self):
        """Agent must raise ValueError when no API key is available."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("OPENAI_API_KEY", None)
            with self.assertRaises(ValueError):
                BusinessGrowthAgent(api_key="")

    def test_accepts_api_key_arg(self):
        agent = BusinessGrowthAgent(api_key="sk-test")
        self.assertIsNotNone(agent)

    def test_accepts_env_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-env-test"}):
            agent = BusinessGrowthAgent()
            self.assertIsNotNone(agent)

    def test_default_model(self):
        agent = BusinessGrowthAgent(api_key="sk-test")
        self.assertEqual(agent.model, "gpt-4o-mini")

    def test_custom_model(self):
        agent = BusinessGrowthAgent(api_key="sk-test", model="gpt-4o")
        self.assertEqual(agent.model, "gpt-4o")


class TestChatMethod(unittest.TestCase):
    def setUp(self):
        self.agent = BusinessGrowthAgent(api_key="sk-test")

    def test_chat_returns_string(self):
        result = self.agent.chat("Hello")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_history_grows_on_chat(self):
        self.agent.chat("First message")
        self.agent.chat("Second message")
        # Each call adds 1 user + 1 assistant turn → history should have 4 entries
        self.assertEqual(len(self.agent._history), 4)

    def test_reset_history_clears_history(self):
        self.agent.chat("Something")
        self.agent.reset_history()
        self.assertEqual(len(self.agent._history), 0)

    def test_chat_with_reset_history_flag(self):
        self.agent.chat("First")
        self.agent.chat("Second", reset_history=True)
        # Only the second turn should be in history
        self.assertEqual(len(self.agent._history), 2)


class TestCapabilityMethods(unittest.TestCase):
    """Verify that each capability method calls chat() and returns a string."""

    def setUp(self):
        self.agent = BusinessGrowthAgent(api_key="sk-test")

    def _assert_returns_str(self, result):
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_social_media_content(self):
        result = self.agent.social_media_content(
            business_type="cafe",
            location="Pune",
            target_audience="college students",
        )
        self._assert_returns_str(result)

    def test_social_media_content_clamps_num_posts(self):
        """num_posts should be clamped to 1-5."""
        with patch.object(self.agent, "chat", return_value="ok") as mock_chat:
            self.agent.social_media_content(
                business_type="cafe",
                location="Pune",
                target_audience="all",
                num_posts=10,  # should be clamped to 5
            )
            call_args = mock_chat.call_args[0][0]
            self.assertIn("5", call_args)

    def test_growth_strategy(self):
        result = self.agent.growth_strategy(
            business_type="restaurant",
            location="Delhi",
            problem="low footfall on weekdays",
        )
        self._assert_returns_str(result)

    def test_analyze_reviews_list_input(self):
        result = self.agent.analyze_reviews(
            business_type="salon",
            location="Mumbai",
            reviews=["Great service!", "Too expensive.", "Will come again."],
        )
        self._assert_returns_str(result)

    def test_analyze_reviews_string_input(self):
        result = self.agent.analyze_reviews(
            business_type="cafe",
            location="Hyderabad",
            reviews="Coffee was amazing!\nPrices are a bit high.",
        )
        self._assert_returns_str(result)

    def test_analyze_reviews_empty_returns_warning(self):
        result = self.agent.analyze_reviews(
            business_type="cafe",
            location="Chennai",
            reviews=[],
        )
        self.assertIn("No reviews provided", result)

    def test_performance_report(self):
        result = self.agent.performance_report(
            business_type="bakery",
            location="Ahmedabad",
            footfall=250,
            revenue=45000,
            new_customers=40,
            repeat_customers=210,
            top_item="Chocolate cake",
        )
        self._assert_returns_str(result)

    def test_customer_personas(self):
        result = self.agent.customer_personas(
            business_type="boutique",
            location="Jaipur",
            avg_transaction=800,
            peak_hours="11 AM – 1 PM and 5 PM – 7 PM",
        )
        self._assert_returns_str(result)

    def test_pricing_and_offers(self):
        result = self.agent.pricing_and_offers(
            business_type="cafe",
            location="Bangalore",
            current_pricing="cappuccino ₹120, sandwich ₹90",
            goal="increase average order value",
        )
        self._assert_returns_str(result)

    def test_daily_action_plan(self):
        result = self.agent.daily_action_plan(
            business_type="salon",
            location="Kolkata",
            focus_area="Instagram growth",
            available_time=3.0,
            budget=500,
        )
        self._assert_returns_str(result)

    def test_instagram_content(self):
        result = self.agent.instagram_content(
            business_type="cafe",
            location="Koramangala, Bangalore",
            audience="college students",
        )
        self._assert_returns_str(result)

    def test_solve_business_problem(self):
        result = self.agent.solve_business_problem(
            problem="Footfall has dropped 40% since a new competitor opened nearby",
            details="Cafe in Indiranagar, Bangalore; budget ₹5,000/month; 2 staff",
        )
        self._assert_returns_str(result)


# ---------------------------------------------------------------------------
# Prompt template tests
# ---------------------------------------------------------------------------

class TestPromptTemplates(unittest.TestCase):
    def test_system_prompt_contains_key_instructions(self):
        self.assertIn("Quick Win", SYSTEM_PROMPT)
        self.assertIn("Mistake to Avoid", SYSTEM_PROMPT)
        self.assertIn("India", SYSTEM_PROMPT)
        self.assertIn("bullet points", SYSTEM_PROMPT)

    def test_social_media_prompt_has_required_placeholders(self):
        for key in ("business_type", "location", "target_audience", "platform",
                    "theme", "tone", "num_posts"):
            self.assertIn(f"{{{key}}}", SOCIAL_MEDIA_PROMPT)

    def test_growth_strategy_prompt_has_required_placeholders(self):
        for key in ("business_type", "location", "monthly_revenue", "problem",
                    "marketing_budget"):
            self.assertIn(f"{{{key}}}", GROWTH_STRATEGY_PROMPT)

    def test_review_prompt_has_reviews_placeholder(self):
        self.assertIn("{reviews}", REVIEW_ANALYSIS_PROMPT)

    def test_performance_report_prompt_completeness(self):
        for key in ("footfall", "revenue", "new_customers", "repeat_customers",
                    "top_item", "social_reach"):
            self.assertIn(f"{{{key}}}", PERFORMANCE_REPORT_PROMPT)

    def test_persona_prompt_completeness(self):
        for key in ("avg_transaction", "peak_hours", "observations"):
            self.assertIn(f"{{{key}}}", PERSONA_PROMPT)

    def test_pricing_prompt_completeness(self):
        for key in ("current_pricing", "competitor_pricing", "goal"):
            self.assertIn(f"{{{key}}}", PRICING_PROMPT)

    def test_action_plan_prompt_completeness(self):
        for key in ("focus_area", "available_time", "budget"):
            self.assertIn(f"{{{key}}}", ACTION_PLAN_PROMPT)

    def test_instagram_content_prompt_has_required_placeholders(self):
        for key in ("business_type", "location", "audience"):
            self.assertIn(f"{{{key}}}", INSTAGRAM_CONTENT_PROMPT)

    def test_instagram_content_prompt_has_required_sections(self):
        for section in ("Instagram Post", "Caption", "Hashtags", "Reel Idea"):
            self.assertIn(section, INSTAGRAM_CONTENT_PROMPT)

    def test_problem_solver_prompt_has_required_placeholders(self):
        for key in ("problem", "details"):
            self.assertIn(f"{{{key}}}", PROBLEM_SOLVER_PROMPT)

    def test_problem_solver_prompt_has_required_sections(self):
        for section in ("3 Actionable Strategies", "Quick Win",
                        "Long-Term Strategy", "Mistake to Avoid"):
            self.assertIn(section, PROBLEM_SOLVER_PROMPT)


if __name__ == "__main__":
    unittest.main()
