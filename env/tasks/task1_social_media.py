"""Task 1 — Social Media Growth (Easy, 10 steps).

Goal: grow followers to ≥ 1 000 and engagement_rate to ≥ 0.05.

Valid actions
-------------
generate_post   quality (1-5)
add_hashtags    count   (1-10)
schedule_post   timing  ("morning" | "evening" | "peak")
run_ad          budget  (int ₹)
no_op           –
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from env.tasks.base_task import BaseTask


class SocialMediaTask(BaseTask):
    TASK_ID = 1
    DESCRIPTION = (
        "Grow your social media following from 500 to 1_000+ followers "
        "and raise engagement rate above 5 %."
    )
    MAX_STEPS = 10

    # Targets
    TARGET_FOLLOWERS = 1_000
    TARGET_ENGAGEMENT = 0.05

    def initial_state(self, rng: Any) -> Dict[str, Any]:
        return {
            "followers": 500,
            "engagement_rate": 0.02,
            "posts_this_week": 0,
            "hashtag_quality": 0.5,
            "post_timing_score": 0.5,
            "market_context": {},
        }

    def get_valid_actions(self) -> List[str]:
        return ["generate_post", "add_hashtags", "schedule_post", "run_ad", "no_op"]

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
        audience_boost = (
            0.05
            if any(
                word in str(market.get("priority_channels", []))
                for word in ["Instagram", "Reels"]
            )
            else 0.0
        )

        spam_penalty = self._spam_count(action_type, action_history) >= 3

        if action_type == "generate_post":
            quality = self._safe_int(
                parameters.get("quality"), default=3, minimum=1, maximum=5
            )
            base_gain = quality * 15
            if spam_penalty:
                base_gain = max(0, base_gain - 10)
            multiplier = (
                s["hashtag_quality"] * s["post_timing_score"] * 2 + audience_boost
            )
            if any(
                token in season_signal
                for token in ["festive", "diwali", "summer", "exam"]
            ):
                multiplier += 0.10
            s["followers"] += int(base_gain * multiplier)
            s["engagement_rate"] = min(
                0.20, s["engagement_rate"] + quality * 0.006 * s["hashtag_quality"]
            )
            s["posts_this_week"] += 1

        elif action_type == "add_hashtags":
            count = self._safe_int(
                parameters.get("count"), default=5, minimum=1, maximum=10
            )
            s["hashtag_quality"] = min(1.0, s["hashtag_quality"] + count * 0.04)

        elif action_type == "schedule_post":
            timing = str(parameters.get("timing", "morning")).lower()
            bonuses = {"morning": 0.10, "evening": 0.15, "peak": 0.25}
            s["post_timing_score"] = min(
                1.0, s["post_timing_score"] + bonuses.get(timing, 0.05)
            )

        elif action_type == "run_ad":
            budget = self._safe_int(
                parameters.get("budget"), default=500, minimum=0, maximum=100_000
            )
            follower_gain = (budget // 100) * 20
            if spam_penalty:
                follower_gain = follower_gain // 2
            s["followers"] += follower_gain
            s["engagement_rate"] = min(0.20, s["engagement_rate"] + 0.003)

        elif action_type == "no_op":
            pass  # no change — penalised in reward

        goal_reached = (
            s["followers"] >= self.TARGET_FOLLOWERS
            and s["engagement_rate"] >= self.TARGET_ENGAGEMENT
        )
        return s, goal_reached

    def _spam_count(self, action_type: str, history: List[str]) -> int:
        """Count consecutive occurrences of action_type at the end of history."""
        count = 0
        for a in reversed(history):
            if a == action_type:
                count += 1
            else:
                break
        return count

    def _safe_int(self, value: Any, default: int, minimum: int, maximum: int) -> int:
        try:
            parsed = int(value)
        except Exception:
            parsed = default
        return max(minimum, min(maximum, parsed))

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        followers_score = min(
            1.0, (state.get("followers", 500) - 500) / (self.TARGET_FOLLOWERS - 500)
        )
        engagement_score = min(
            1.0, state.get("engagement_rate", 0.0) / self.TARGET_ENGAGEMENT
        )
        efficiency_score = max(0.0, 1.0 - steps_used / self.MAX_STEPS)
        return round(
            0.40 * followers_score + 0.40 * engagement_score + 0.20 * efficiency_score,
            4,
        )
