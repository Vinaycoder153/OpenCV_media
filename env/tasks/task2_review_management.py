"""Task 2 — Review Management (Medium, 12 steps).

Goal: raise avg_rating to ≥ 4.0 and sentiment_score to ≥ 0.7.

Valid actions
-------------
reply_review      tone    ("professional" | "apologetic" | "friendly")
request_review    channel ("sms" | "email" | "in-person")
offer_discount    value   (int %, e.g. 10)
improve_service   area    (str, e.g. "speed" | "quality" | "cleanliness")
no_op             –
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from env.tasks.base_task import BaseTask


class ReviewManagementTask(BaseTask):
    TASK_ID = 2
    DESCRIPTION = (
        "Improve your average rating from 3.2 to 4.0+ and raise the "
        "customer sentiment score above 0.7."
    )
    MAX_STEPS = 12

    TARGET_RATING = 4.0
    TARGET_SENTIMENT = 0.7

    def initial_state(self, rng: Any) -> Dict[str, Any]:
        return {
            "avg_rating": 3.2,
            "total_reviews": 15,
            "positive_reviews": 7,
            "replied_reviews": 0,
            "sentiment_score": 0.40,
            "service_quality": 0.55,
            "market_context": {},
        }

    def get_valid_actions(self) -> List[str]:
        return [
            "reply_review",
            "request_review",
            "offer_discount",
            "improve_service",
            "no_op",
        ]

    def apply_action(
        self,
        state: Dict[str, Any],
        action_type: str,
        parameters: Dict[str, Any],
        rng: Any,
        action_history: List[str],
    ) -> Tuple[Dict[str, Any], bool]:
        s = copy.deepcopy(state)
        market = (
            s.get("market_context", {})
            if isinstance(s.get("market_context"), dict)
            else {}
        )
        season_signal = str(market.get("season_signal", "")).lower()

        repeat_count = self._repeat_count(action_type, action_history)
        diminish = max(0.2, 1.0 - repeat_count * 0.15)  # diminishing returns

        if action_type == "reply_review":
            tone_boost = {"professional": 0.09, "apologetic": 0.07, "friendly": 0.08}
            tone = str(parameters.get("tone", "professional")).lower()
            boost = tone_boost.get(tone, 0.06) * diminish
            if any(
                token in season_signal for token in ["festival", "diwali", "holiday"]
            ):
                boost += 0.02
            s["sentiment_score"] = min(1.0, s["sentiment_score"] + boost)
            s["replied_reviews"] = min(s["total_reviews"], s["replied_reviews"] + 1)
            # Positive replies slowly improve the rating
            s["avg_rating"] = min(5.0, s["avg_rating"] + 0.04 * diminish)

        elif action_type == "request_review":
            channel_new = {"sms": 2, "email": 1, "in-person": 3}
            channel = str(parameters.get("channel", "sms")).lower()
            new_positive = int(channel_new.get(channel, 1) * diminish)
            s["positive_reviews"] += new_positive
            s["total_reviews"] += new_positive + 1
            # Recompute rating
            neg_reviews = s["total_reviews"] - s["positive_reviews"]
            s["avg_rating"] = min(
                5.0,
                (s["positive_reviews"] * 4.5 + neg_reviews * 2.0) / s["total_reviews"],
            )
            s["sentiment_score"] = min(
                1.0,
                s["positive_reviews"] / s["total_reviews"],
            )

        elif action_type == "offer_discount":
            value = self._safe_int(
                parameters.get("value"), default=10, minimum=5, maximum=30
            )
            # Discount drives new positive reviews
            new_positive = int((value / 10) * diminish)
            s["positive_reviews"] += new_positive
            s["total_reviews"] += new_positive + 1
            neg_reviews = s["total_reviews"] - s["positive_reviews"]
            s["avg_rating"] = min(
                5.0,
                (s["positive_reviews"] * 4.5 + neg_reviews * 2.0) / s["total_reviews"],
            )
            s["sentiment_score"] = min(1.0, s["positive_reviews"] / s["total_reviews"])

        elif action_type == "improve_service":
            area = str(parameters.get("area", "quality")).lower()
            area_boosts = {
                "speed": 0.08,
                "quality": 0.10,
                "cleanliness": 0.07,
                "staff": 0.09,
            }
            boost = area_boosts.get(area, 0.07) * diminish
            if any(
                token in season_signal for token in ["monsoon", "summer", "festival"]
            ):
                boost += 0.01
            s["service_quality"] = min(1.0, s["service_quality"] + boost)
            s["sentiment_score"] = min(1.0, s["sentiment_score"] + boost * 1.5)
            s["avg_rating"] = min(5.0, s["avg_rating"] + boost * 0.8)

        elif action_type == "no_op":
            pass

        goal_reached = (
            s["avg_rating"] >= self.TARGET_RATING
            and s["sentiment_score"] >= self.TARGET_SENTIMENT
        )
        return s, goal_reached

    def _safe_int(self, value: Any, default: int, minimum: int, maximum: int) -> int:
        try:
            parsed = int(value)
        except Exception:
            parsed = default
        return max(minimum, min(maximum, parsed))

    def _repeat_count(self, action_type: str, history: List[str]) -> int:
        count = 0
        for a in reversed(history):
            if a == action_type:
                count += 1
            else:
                break
        return count

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        rating_score = max(
            0.0, (state.get("avg_rating", 3.2) - 3.2) / (self.TARGET_RATING - 3.2)
        )
        sentiment_score = state.get("sentiment_score", 0.0)
        reply_coverage = state.get("replied_reviews", 0) / max(
            1, state.get("total_reviews", 1)
        )
        efficiency_score = max(0.0, 1.0 - steps_used / self.MAX_STEPS)
        return round(
            0.40 * min(1.0, rating_score)
            + 0.35 * min(1.0, sentiment_score)
            + 0.25 * min(1.0, reply_coverage),
            4,
        )
