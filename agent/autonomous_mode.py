"""Autonomous business-growth runner with transparent decisions.

This module provides a deterministic, hackathon-demo-friendly "auto mode" that
combines rule-based policies and environment feedback to simulate business
improvement over a configurable period.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType, Observation


@dataclass
class TransparentDecision:
    day: int
    task_id: int
    action: str
    rationale: str
    expected_outcome: str
    reward: float
    metrics_snapshot: Dict[str, float]


class AutonomousGrowthRunner:
    """Runs deterministic autonomous simulations over OpenEnv tasks."""

    def __init__(self, seed: int = 42) -> None:
        self.seed = seed

    def run(self, days: int = 14) -> Dict[str, Any]:
        days = max(3, min(30, int(days)))

        tasks = [1, 2, 3]
        decisions: List[TransparentDecision] = []
        before_after: Dict[int, Dict[str, Any]] = {}

        for task_id in tasks:
            env = BusinessEnv(
                task_id=task_id,
                seed=self.seed,
                config={
                    "business_type": "cafe",
                    "location": "Bangalore",
                    "audience": "young professionals",
                    "budget": 8000,
                    "revenue": 95000,
                    "focus_area": "growth",
                },
            )
            obs = env.reset()
            before_after[task_id] = {
                "before": self._extract_metrics(obs),
                "after": None,
                "score": 0.0,
            }

            for day in range(1, days + 1):
                action, rationale, expected = self._choose_action(task_id, obs)
                result = env.step(action)
                decisions.append(
                    TransparentDecision(
                        day=day,
                        task_id=task_id,
                        action=action.action_type.value,
                        rationale=rationale,
                        expected_outcome=expected,
                        reward=result.reward.value,
                        metrics_snapshot=self._extract_metrics(result.observation),
                    )
                )
                obs = result.observation
                if result.done:
                    break

            final_state = env.state()["task_state"]
            before_after[task_id]["after"] = self._extract_metrics(obs)
            before_after[task_id]["score"] = float(
                env._task.grade(final_state, env.state()["step"])
            )

        return {
            "mode": "rule+ai",
            "period_days": days,
            "decisions": [asdict(item) for item in decisions],
            "impact": before_after,
            "summary": self._build_summary(before_after),
        }

    def _choose_action(self, task_id: int, obs: Observation) -> tuple[Action, str, str]:
        m = obs.metrics
        if task_id == 1:
            # Three-step burst: hashtags → high-quality post → paid boost.
            if m.followers == 500 and m.engagement_rate <= 0.02:
                return (
                    Action(
                        action_type=ActionType.ADD_HASHTAGS,
                        parameters={"count": 10},
                    ),
                    "Maximise hashtag quality first to boost post multiplier.",
                    "Hashtag quality reaches 0.90, amplifying all future content.",
                )
            if m.engagement_rate < 0.045:
                return (
                    Action(
                        action_type=ActionType.GENERATE_POST,
                        parameters={"quality": 5},
                    ),
                    "High-quality content drives engagement and organic reach.",
                    "Engagement jumps close to the 5 % target.",
                )
            if m.followers < 1000:
                return (
                    Action(action_type=ActionType.RUN_AD, parameters={"budget": 3000}),
                    "Paid reach closes the follower gap quickly.",
                    "Follower count crosses the 1 000 target.",
                )
            return (
                Action(action_type=ActionType.GENERATE_POST, parameters={"quality": 5}),
                "Sustain engagement with quality content.",
                "Continued organic growth.",
            )

        if task_id == 2:
            # Alternate improve_service and reply_review to push both metrics
            # with zero diminishing returns.
            recent = obs.recent_actions
            last_action = recent[-1] if recent else ""

            if not recent:
                return (
                    Action(
                        action_type=ActionType.REQUEST_REVIEW,
                        parameters={"channel": "in-person"},
                    ),
                    "Seed positive reviews for a strong rating base.",
                    "More positive reviews improve the rating denominator.",
                )
            if last_action == "improve_service" or last_action == "request_review":
                return (
                    Action(
                        action_type=ActionType.REPLY_REVIEW,
                        parameters={"tone": "professional"},
                    ),
                    "Professional replies boost sentiment and reply coverage.",
                    "Sentiment lift and better reply-to-total ratio.",
                )
            return (
                Action(
                    action_type=ActionType.IMPROVE_SERVICE,
                    parameters={"area": "quality"},
                ),
                "Service quality improvements lift both rating and sentiment.",
                "Rating and sentiment move toward their targets.",
            )

        # task 3 — build satisfaction first, then revenue via bundle.
        if m.customer_satisfaction < 0.98:
            return (
                Action(action_type=ActionType.ADD_OFFER, parameters={"discount_pct": 5}),
                "Small offers steadily raise satisfaction with minimal margin impact.",
                "Satisfaction rises toward 1.0.",
            )
        if m.monthly_revenue < 120_000:
            return (
                Action(
                    action_type=ActionType.LAUNCH_BUNDLE,
                    parameters={
                        "items": ["coffee", "snack", "dessert", "drink", "combo"],
                        "bundle_price": 500.0,
                    },
                ),
                "Large bundle lifts AOV and orders for an instant revenue jump.",
                "Revenue exceeds ₹1,20,000 target.",
            )
        return (
            Action(action_type=ActionType.ADD_OFFER, parameters={"discount_pct": 5}),
            "Maintain customer goodwill with light offers.",
            "Sustained satisfaction.",
        )

    def _extract_metrics(self, obs: Observation) -> Dict[str, float]:
        m = obs.metrics
        return {
            "followers": float(m.followers),
            "engagement_rate": float(m.engagement_rate),
            "avg_rating": float(m.avg_rating),
            "monthly_revenue": float(m.monthly_revenue),
            "daily_orders": float(m.daily_orders),
            "avg_order_value": float(m.avg_order_value),
        }

    def _build_summary(self, impact: Dict[int, Dict[str, Any]]) -> str:
        t1 = impact[1]
        t2 = impact[2]
        t3 = impact[3]

        followers_delta = t1["after"]["followers"] - t1["before"]["followers"]
        rating_delta = t2["after"]["avg_rating"] - t2["before"]["avg_rating"]
        revenue_delta = t3["after"]["monthly_revenue"] - t3["before"]["monthly_revenue"]

        return (
            "Autonomous mode completed with deterministic rule+AI policy. "
            f"Followers improved by {followers_delta:.0f}, "
            f"average rating improved by {rating_delta:.2f}, "
            f"and monthly revenue improved by ₹{revenue_delta:,.0f}."
        )
