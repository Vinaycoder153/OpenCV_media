"""Core OpenEnv environment: BusinessEnv.

Interface
---------
env = BusinessEnv(task_id=1, seed=42)
obs  = env.reset()                    # → Observation
result = env.step(action)             # → StepResult (obs, reward, done, info)
state = env.state()                   # → dict
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from agent.intelligence import build_business_context
from env.models.schemas import (
    Action,
    ActionType,
    BusinessProfile,
    BusinessMetrics,
    Observation,
    MarketContext,
    Reward,
    StepResult,
)
from env.tasks.base_task import BaseTask
from env.tasks.task1_social_media import SocialMediaTask
from env.tasks.task2_review_management import ReviewManagementTask
from env.tasks.task3_revenue_optimization import RevenueOptimizationTask

_TASKS: Dict[int, type] = {
    1: SocialMediaTask,
    2: ReviewManagementTask,
    3: RevenueOptimizationTask,
}

_TASK_DESCRIPTIONS = {
    1: "Social Media Growth (Easy) — 10 steps",
    2: "Review Management (Medium) — 12 steps",
    3: "Revenue Optimization (Hard) — 15 steps",
}


class BusinessEnv:
    """
    OpenEnv-compliant environment simulating small-business growth.

    Parameters
    ----------
    task_id : int
        1 = Social Media Growth (Easy)
        2 = Review Management (Medium)
        3 = Revenue Optimization (Hard)
    config : dict, optional
        Override task/reward parameters.
    seed : int
        Random seed for deterministic behaviour.
    """

    def __init__(
        self,
        task_id: int = 1,
        config: Optional[Dict[str, Any]] = None,
        seed: int = 42,
    ) -> None:
        if task_id not in _TASKS:
            raise ValueError(f"task_id must be 1, 2, or 3. Got {task_id}.")
        self._task_id = task_id
        self._config = config or {}
        self._seed = seed
        self._rng = random.Random(seed)

        self._task: BaseTask = _TASKS[task_id]()
        self._state: Dict[str, Any] = {}
        self._profile = build_business_context(
            business_type=self._config.get("business_type", "business"),
            location=self._config.get("location", "India"),
            audience=self._config.get("audience", ""),
            budget=self._config.get("budget", 0),
            revenue=self._config.get("revenue", 0),
            focus_area=self._config.get("focus_area", ""),
            problem=self._config.get("problem", ""),
        )
        self._step_count: int = 0
        self._action_history: List[str] = []
        self._done: bool = False

    # ------------------------------------------------------------------
    # OpenEnv interface
    # ------------------------------------------------------------------

    def reset(self) -> Observation:
        """Reset environment to initial state and return the first observation."""
        self._rng = random.Random(self._seed)
        self._state = self._task.initial_state(self._rng)
        self._state["business_profile"] = self._profile.business_type
        self._state["location"] = self._profile.location
        self._state["market_context"] = {
            "city_tier": self._profile.city_tier,
            "season_signal": self._profile.season_signal,
            "priority_channels": self._profile.channel_priority,
            "risk_flags": self._profile.risk_flags,
        }
        self._step_count = 0
        self._action_history = []
        self._done = False
        return self._build_observation(hint="Use reset() to start a new episode.")

    def step(self, action: Action) -> StepResult:
        """Apply *action*, advance state, compute reward.

        Returns
        -------
        StepResult with (observation, reward, done, info).
        """
        if self._done:
            obs = self._build_observation(
                hint="Episode already finished. Call reset()."
            )
            return StepResult(
                observation=obs,
                reward=Reward(value=0.0, reason="Episode already done."),
                done=True,
                info={"warning": "step() called after episode ended"},
            )

        if action.action_type.value not in self._task.get_valid_actions():
            obs = self._build_observation(
                hint="Invalid action ignored. Choose one of the valid actions listed in the observation."
            )
            reward = Reward(
                value=-0.2,
                components={"invalid_action_penalty": -0.2},
                reason=f"invalid action: {action.action_type.value}",
            )
            self._step_count += 1
            self._action_history.append("no_op")
            self._done = self._step_count >= self._task.MAX_STEPS
            return StepResult(
                observation=obs,
                reward=reward,
                done=self._done,
                info={"warning": "invalid action ignored", "step": self._step_count},
            )

        prev_state = dict(self._state)
        action_str = action.action_type.value

        # Apply action
        new_state, goal_reached = self._task.apply_action(
            self._state,
            action_str,
            action.parameters,
            self._rng,
            self._action_history,
        )
        self._state = new_state
        self._step_count += 1
        self._action_history.append(action_str)

        # Check termination
        max_steps_reached = self._step_count >= self._task.MAX_STEPS
        self._done = goal_reached or max_steps_reached

        # Compute reward
        reward = self._compute_reward(prev_state, new_state, action_str, goal_reached)

        obs = self._build_observation()
        info: Dict[str, Any] = {
            "step": self._step_count,
            "goal_reached": goal_reached,
            "max_steps_reached": max_steps_reached,
            "final_score": (
                self._task.grade(self._state, self._step_count) if self._done else None
            ),
        }
        return StepResult(observation=obs, reward=reward, done=self._done, info=info)

    def state(self) -> Dict[str, Any]:
        """Return the full internal state dict (read-only copy)."""
        return {
            "task_id": self._task_id,
            "step": self._step_count,
            "done": self._done,
            "task_state": dict(self._state),
            "action_history": list(self._action_history),
        }

    # ------------------------------------------------------------------
    # Reward computation
    # ------------------------------------------------------------------

    def _compute_reward(
        self,
        prev: Dict[str, Any],
        curr: Dict[str, Any],
        action_str: str,
        goal_reached: bool,
    ) -> Reward:
        components: Dict[str, float] = {}
        reason_parts: List[str] = []

        # ── No-op penalty ──────────────────────────────────────────────
        if action_str == "no_op":
            components["no_op_penalty"] = -0.10
            reason_parts.append("no-op")

        # ── Spam penalty ───────────────────────────────────────────────
        spam_run = 0
        for a in reversed(self._action_history[:-1]):  # history before this step
            if a == action_str:
                spam_run += 1
            else:
                break
        if spam_run >= 2:
            components["spam_penalty"] = -0.05 * (spam_run - 1)
            reason_parts.append(f"spam×{spam_run}")

        # ── Progress rewards ───────────────────────────────────────────
        if self._task_id == 1:
            follower_delta = curr.get("followers", 0) - prev.get("followers", 0)
            eng_delta = curr.get("engagement_rate", 0.0) - prev.get(
                "engagement_rate", 0.0
            )
            prog = follower_delta / 500 + eng_delta / 0.05
            if prog > 0:
                components["progress"] = round(prog * 0.5, 4)
                reason_parts.append("follower/engagement gain")
            elif prog < 0:
                components["destructive"] = round(prog * 0.3, 4)
                reason_parts.append("metric dropped")

        elif self._task_id == 2:
            rating_delta = curr.get("avg_rating", 0.0) - prev.get("avg_rating", 0.0)
            sent_delta = curr.get("sentiment_score", 0.0) - prev.get(
                "sentiment_score", 0.0
            )
            prog = rating_delta / 0.8 + sent_delta / 0.30
            if prog > 0:
                components["progress"] = round(prog * 0.4, 4)
                reason_parts.append("rating/sentiment gain")

        elif self._task_id == 3:
            rev_delta = curr.get("monthly_revenue", 0.0) - prev.get(
                "monthly_revenue", 0.0
            )
            sat_delta = curr.get("customer_satisfaction", 0.0) - prev.get(
                "customer_satisfaction", 0.0
            )
            prog = rev_delta / 40_000 + sat_delta / 0.30
            if prog > 0:
                components["progress"] = round(prog * 0.6, 4)
                reason_parts.append("revenue/satisfaction gain")
            elif rev_delta < -5_000:
                components["destructive"] = round(rev_delta / 40_000 * 0.5, 4)
                reason_parts.append("revenue drop")

        # ── Goal bonus ─────────────────────────────────────────────────
        if goal_reached:
            components["goal_bonus"] = 1.0
            reason_parts.append("GOAL REACHED")

        # Terminal shaping nudges the agent toward completing tasks efficiently.
        if self._done:
            final_score = self._task.grade(curr, self._step_count)
            terminal_bonus = round(max(0.0, final_score - 0.5), 4)
            if terminal_bonus:
                components["terminal_bonus"] = terminal_bonus
                reason_parts.append(f"terminal={terminal_bonus:+.2f}")

        total = round(sum(components.values()), 4)
        return Reward(
            value=total,
            components=components,
            reason=" | ".join(reason_parts) if reason_parts else "no change",
            terminal_bonus=components.get("terminal_bonus", 0.0),
        )

    # ------------------------------------------------------------------
    # Observation builder
    # ------------------------------------------------------------------

    def _build_observation(self, hint: Optional[str] = None) -> Observation:
        metrics = self._state_to_metrics()
        trend = self._compute_trend()
        return Observation(
            task_id=self._task_id,
            step=self._step_count,
            metrics=metrics,
            recent_actions=list(self._action_history[-5:]),
            trend=trend,
            task_description=self._task.DESCRIPTION,
            valid_actions=self._task.get_valid_actions(),
            hint=hint,
            business_profile=BusinessProfile(
                business_type=self._profile.business_type,
                location=self._profile.location,
                audience=self._profile.audience,
                budget_band=(
                    "tight"
                    if self._profile.budget < 1500
                    else "standard" if self._profile.budget < 10000 else "premium"
                ),
                pricing_position=(
                    "value" if self._profile.budget < 2000 else "mid-market"
                ),
            ),
            market_context=MarketContext(
                city_tier=self._profile.city_tier,
                season_signal=self._profile.season_signal,
                priority_channels=self._profile.channel_priority,
                risk_flags=self._profile.risk_flags,
            ),
        )

    def _state_to_metrics(self) -> BusinessMetrics:
        s = self._state
        return BusinessMetrics(
            followers=s.get("followers", 0),
            engagement_rate=s.get("engagement_rate", 0.0),
            avg_rating=s.get("avg_rating", 0.0),
            total_reviews=s.get("total_reviews", 0),
            positive_reviews=s.get("positive_reviews", 0),
            monthly_revenue=s.get("monthly_revenue", 0.0),
            daily_orders=s.get("daily_orders", 0),
            avg_order_value=s.get("avg_order_value", 0.0),
        )

    def _compute_trend(self) -> str:
        if len(self._action_history) < 2:
            return "stable"
        if self._task_id == 1:
            return "growing" if self._state.get("followers", 0) > 500 else "stable"
        if self._task_id == 2:
            return "improving" if self._state.get("avg_rating", 0) > 3.2 else "stable"
        if self._task_id == 3:
            return (
                "growing"
                if self._state.get("monthly_revenue", 0) > 80_000
                else "stable"
            )
        return "stable"
