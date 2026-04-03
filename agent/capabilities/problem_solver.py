"""Business problem solver capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agent.intelligence import build_business_context, build_context_brief
from agent.prompts import PROBLEM_SOLVER_PROMPT

if TYPE_CHECKING:
    from agent.business_agent import BusinessGrowthAgent


def solve_business_problem(
    agent: "BusinessGrowthAgent",
    problem: str,
    details: str,
) -> str:
    """
    Generate low-budget, high-impact solutions for a specific business problem.

    Parameters
    ----------
    agent:
        The :class:`BusinessGrowthAgent` instance providing the LLM client.
    problem:
        A concise description of the business problem to solve, e.g.
        "footfall has dropped 40% since a new competitor opened nearby".
    details:
        Relevant business details (type, location, budget, team size, etc.).

    Returns
    -------
    str
        Structured output with 3 actionable strategies, 1 quick win,
        1 long-term strategy, and 1 mistake to avoid.
    """
    context = build_business_context(
        business_type="business",
        location="India",
        problem=problem,
        focus_area="problem solving",
    )
    prompt = PROBLEM_SOLVER_PROMPT.format(
        problem=problem,
        details=details,
    )
    return agent.chat_with_context(prompt, build_context_brief(context))
