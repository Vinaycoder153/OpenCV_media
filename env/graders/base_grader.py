"""Abstract base grader."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseGrader(ABC):
    """Score a completed episode on a 0.0–1.0 scale.

    Thresholds
    ----------
    poor    < 0.4
    average  0.4 – 0.7
    good    > 0.7
    """

    @abstractmethod
    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        """Return a score in [0.0, 1.0]."""

    @staticmethod
    def label(score: float) -> str:
        if score < 0.4:
            return "poor"
        if score <= 0.7:
            return "average"
        return "good"
