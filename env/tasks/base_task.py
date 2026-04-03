"""Abstract base class for all OpenEnv tasks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple


class BaseTask(ABC):
    """Every task must implement these methods."""

    TASK_ID: int = 0
    DESCRIPTION: str = ""
    MAX_STEPS: int = 10

    @abstractmethod
    def initial_state(self, rng: Any) -> Dict[str, Any]:
        """Return the starting state dict for this task."""

    @abstractmethod
    def apply_action(
        self,
        state: Dict[str, Any],
        action_type: str,
        parameters: Dict[str, Any],
        rng: Any,
        action_history: List[str],
    ) -> Tuple[Dict[str, Any], bool]:
        """
        Apply *action* to *state* and return (new_state, goal_reached).

        Parameters
        ----------
        state:          Current mutable state dict (will be copied internally).
        action_type:    The ActionType value string.
        parameters:     Action parameters dict.
        rng:            A ``random.Random`` instance for deterministic noise.
        action_history: List of previous action_type strings this episode.

        Returns
        -------
        new_state:    Updated state dict.
        goal_reached: True when the task goal is satisfied.
        """

    @abstractmethod
    def get_valid_actions(self) -> List[str]:
        """Return the list of valid ActionType values for this task."""

    @abstractmethod
    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        """
        Score the final state on a 0.0–1.0 scale.

        Thresholds:  poor < 0.4 | average 0.4–0.7 | good > 0.7
        """
