"""Grader for Task 1 — Social Media Growth."""

from __future__ import annotations

from typing import Any, Dict

from env.graders.base_grader import BaseGrader


class SocialMediaGrader(BaseGrader):
    """Score a Social Media Growth episode.

    Components
    ----------
    followers_score  (40 %) — progress from 500 to 1 000
    engagement_score (40 %) — progress to 5 % engagement rate
    efficiency_score (20 %) — unused steps out of MAX_STEPS=10
    """

    TARGET_FOLLOWERS = 1000
    BASE_FOLLOWERS = 500
    TARGET_ENGAGEMENT = 0.05
    MAX_STEPS = 10

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        followers_score = min(
            1.0,
            (state.get("followers", 500) - self.BASE_FOLLOWERS)
            / (self.TARGET_FOLLOWERS - self.BASE_FOLLOWERS),
        )
        engagement_score = min(
            1.0, state.get("engagement_rate", 0.0) / self.TARGET_ENGAGEMENT
        )
        efficiency_score = max(0.0, 1.0 - steps_used / self.MAX_STEPS)
        return round(
            0.40 * max(0.0, followers_score)
            + 0.40 * engagement_score
            + 0.20 * efficiency_score,
            4,
        )
