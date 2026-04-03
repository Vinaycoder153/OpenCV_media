"""Grader for Task 3 — Revenue Optimization."""

from __future__ import annotations

from typing import Any, Dict

from env.graders.base_grader import BaseGrader


class RevenueGrader(BaseGrader):
    """Score a Revenue Optimization episode.

    Components
    ----------
    revenue_score      (50 %) — progress from ₹80 000 to ₹1 20 000
    satisfaction_score (30 %) — final customer_satisfaction
    order_score        (20 %) — daily orders progress from 25 to 40
    """

    BASE_REVENUE = 80_000.0
    TARGET_REVENUE = 120_000.0
    BASE_ORDERS = 25
    TARGET_ORDERS = 40

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        revenue_score = min(
            1.0,
            (state.get("monthly_revenue", self.BASE_REVENUE) - self.BASE_REVENUE)
            / (self.TARGET_REVENUE - self.BASE_REVENUE),
        )
        satisfaction_score = min(1.0, state.get("customer_satisfaction", 0.0))
        order_score = min(
            1.0,
            (state.get("daily_orders", self.BASE_ORDERS) - self.BASE_ORDERS)
            / (self.TARGET_ORDERS - self.BASE_ORDERS),
        )
        return round(
            0.50 * max(0.0, revenue_score)
            + 0.30 * satisfaction_score
            + 0.20 * max(0.0, order_score),
            4,
        )
