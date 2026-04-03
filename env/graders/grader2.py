"""Grader for Task 2 — Review Management."""

from __future__ import annotations

from typing import Any, Dict

from env.graders.base_grader import BaseGrader


class ReviewManagementGrader(BaseGrader):
    """Score a Review Management episode.

    Components
    ----------
    rating_score    (40 %) — progress from 3.2 to 4.0
    sentiment_score (35 %) — final sentiment_score value
    reply_coverage  (25 %) — replied_reviews / total_reviews
    """

    BASE_RATING = 3.2
    TARGET_RATING = 4.0

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        rating_score = max(
            0.0,
            (state.get("avg_rating", 3.2) - self.BASE_RATING)
            / (self.TARGET_RATING - self.BASE_RATING),
        )
        sentiment = state.get("sentiment_score", 0.0)
        total = max(1, state.get("total_reviews", 1))
        replied = state.get("replied_reviews", 0)
        reply_coverage = replied / total
        return round(
            0.40 * min(1.0, rating_score)
            + 0.35 * min(1.0, sentiment)
            + 0.25 * min(1.0, reply_coverage),
            4,
        )
