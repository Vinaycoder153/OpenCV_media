#!/usr/bin/env python3
"""Baseline agent for the AI Business Growth OpenEnv environment.

Modes
-----
* LLM mode  - uses OpenAI-compatible chat completions when API key is set.
* Heuristic mode - runs a rule-based policy with no API calls.

Usage
-----
    export OPENAI_API_KEY="..."   # optional; falls back to heuristic
    python agent/baseline_agent.py
"""

from __future__ import annotations

import logging
import os
import sys
from itertools import cycle
from typing import Any, Dict, List, Optional

# Ensure the repo root is on the path when running directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType
from agent.action_parser import (
    TASK_ACTION_PROMPTS,
    format_observation_for_llm,
    parse_action_from_text,
)
from agent.openai_client import create_openai_client

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Heuristic action sequences per task
# ---------------------------------------------------------------------------

_HEURISTICS: Dict[int, List[Action]] = {
    1: [
        Action(action_type=ActionType.ADD_HASHTAGS, parameters={"count": 8}),
        Action(action_type=ActionType.SCHEDULE_POST, parameters={"timing": "peak"}),
        Action(action_type=ActionType.GENERATE_POST, parameters={"quality": 5}),
        Action(action_type=ActionType.RUN_AD, parameters={"budget": 2000}),
        Action(action_type=ActionType.GENERATE_POST, parameters={"quality": 4}),
    ],
    2: [
        Action(action_type=ActionType.IMPROVE_SERVICE, parameters={"area": "quality"}),
        Action(
            action_type=ActionType.REPLY_REVIEW, parameters={"tone": "professional"}
        ),
        Action(
            action_type=ActionType.REQUEST_REVIEW, parameters={"channel": "in-person"}
        ),
        Action(action_type=ActionType.REPLY_REVIEW, parameters={"tone": "friendly"}),
        Action(action_type=ActionType.OFFER_DISCOUNT, parameters={"value": 15}),
        Action(action_type=ActionType.IMPROVE_SERVICE, parameters={"area": "speed"}),
    ],
    3: [
        Action(
            action_type=ActionType.RUN_CAMPAIGN,
            parameters={"type": "social", "budget": 5000},
        ),
        Action(action_type=ActionType.ADD_OFFER, parameters={"discount_pct": 15}),
        Action(
            action_type=ActionType.LAUNCH_BUNDLE,
            parameters={"items": ["item1", "item2", "item3"], "bundle_price": 300.0},
        ),
        Action(
            action_type=ActionType.RUN_CAMPAIGN,
            parameters={"type": "email", "budget": 3000},
        ),
    ],
}


# ---------------------------------------------------------------------------
# BaselineAgent
# ---------------------------------------------------------------------------


class BaselineAgent:
    """Baseline agent that can run in LLM or heuristic mode.

    Parameters
    ----------
    task_id   : 1, 2, or 3
    use_llm   : use OpenAI-compatible completion when True and OPENAI_API_KEY is set
    model     : model name (default: "gpt-4o-mini")
    seed      : environment seed for reproducibility
    """

    def __init__(
        self,
        task_id: int,
        use_llm: bool = True,
        model: str = "gpt-4o-mini",
        seed: int = 42,
    ) -> None:
        self.task_id = task_id
        self.model = model
        self.seed = seed

        api_key = os.environ.get("OPENAI_API_KEY", "")
        self.use_llm = use_llm and bool(api_key)
        self._client = None

        if self.use_llm:
            try:
                self._client = create_openai_client(
                    api_key=api_key,
                    base_url=os.environ.get("API_BASE_URL") or None,
                )
            except Exception:
                log.warning(
                    "OpenAI client is unavailable - falling back to heuristic mode."
                )
                self.use_llm = False

        self._env = BusinessEnv(task_id=task_id, seed=seed)

    # ------------------------------------------------------------------
    # Action selection
    # ------------------------------------------------------------------

    def select_action(self, observation: Any, step: int) -> Action:
        """Choose an action given the current observation."""
        if self.use_llm:
            return self._llm_action(observation)
        return self._heuristic_action(step)

    def _llm_action(self, observation: Any) -> Action:
        system_prompt = TASK_ACTION_PROMPTS[self.task_id]
        user_prompt = format_observation_for_llm(observation)

        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
            )
            text = resp.choices[0].message.content or ""
            action = parse_action_from_text(text)
            if action is not None:
                return action
        except Exception as exc:
            log.warning("LLM call failed: %s — using heuristic fallback.", exc)

        # Fallback to heuristic if LLM fails or returns unparseable output
        return self._heuristic_action(0)

    def _heuristic_action(self, step: int) -> Action:
        actions = _HEURISTICS[self.task_id]
        return actions[step % len(actions)]

    # ------------------------------------------------------------------
    # Episode runner
    # ------------------------------------------------------------------

    def run_task(self, max_steps: Optional[int] = None) -> Dict[str, Any]:
        """Run a full episode and return a result summary.

        Returns
        -------
        dict with keys: task_id, steps, actions, rewards, total_reward,
                        final_score, goal_reached
        """
        if not self.use_llm:
            log.info("Heuristic mode (no API key or use_llm=False).")

        obs = self._env.reset()
        actions_log: List[str] = []
        rewards_log: List[float] = []
        goal_reached = False
        step = 0

        while True:
            action = self.select_action(obs, step)
            result = self._env.step(action)

            actions_log.append(action.action_type.value)
            rewards_log.append(result.reward.value)

            log.info(
                "Step %2d | action=%-20s | reward=%+.3f | done=%s",
                result.observation.step,
                action.action_type.value,
                result.reward.value,
                result.done,
            )

            obs = result.observation
            if result.info.get("goal_reached"):
                goal_reached = True
            step += 1

            if result.done:
                final_score = result.info.get("final_score", 0.0)
                break

            if max_steps is not None and step >= max_steps:
                final_score = self._env._task.grade(self._env._state, step)
                break

        return {
            "task_id": self.task_id,
            "steps": step,
            "actions": actions_log,
            "rewards": rewards_log,
            "total_reward": round(sum(rewards_log), 4),
            "final_score": round(final_score, 4),
            "goal_reached": goal_reached,
        }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    log.info("=== AI Business Growth Baseline Agent ===")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    log.info(
        "Mode: %s",
        (
            f"LLM ({os.environ.get('MODEL_NAME', 'gpt-4o-mini')})"
            if api_key
            else "Heuristic (no API key)"
        ),
    )

    results = []
    for task_id in [1, 2, 3]:
        log.info("\n--- Task %d ---", task_id)
        agent = BaselineAgent(task_id=task_id, use_llm=True, seed=42)
        result = agent.run_task()
        results.append(result)

    # Summary table
    print("\n" + "=" * 60)
    print(f"{'Task':<9} {'Steps':<9} {'Score':<11} {'Goal':<11} {'Total Reward'}")
    print("-" * 60)
    for r in results:
        goal_str = "✓" if r["goal_reached"] else "✗"
        print(
            f"Task {r['task_id']:<4} {r['steps']:<9} {r['final_score']:<11.4f} "
            f"{goal_str:<11} {r['total_reward']:+.4f}"
        )
    print("=" * 60)


if __name__ == "__main__":
    main()
