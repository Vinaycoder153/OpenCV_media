"""Task 3 — Revenue Optimization (Hard, 15 steps).

Goal: grow monthly_revenue to ≥ ₹1,20,000 and keep customer_satisfaction ≥ 0.7.

Valid actions
-------------
change_price    direction ("up" | "down"), pct (int %)
add_offer       discount_pct (int %)
run_campaign    type ("social" | "email" | "local"), budget (int ₹)
launch_bundle   items (list[str]), bundle_price (float)
no_op           –
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from env.tasks.base_task import BaseTask


class RevenueOptimizationTask(BaseTask):
    TASK_ID = 3
    DESCRIPTION = (
        "Grow monthly revenue from ₹80,000 to ₹1,20,000+ while keeping "
        "customer satisfaction above 0.7."
    )
    MAX_STEPS = 15

    TARGET_REVENUE = 120_000.0
    TARGET_SATISFACTION = 0.70

    def initial_state(self, rng: Any) -> Dict[str, Any]:
        return {
            "monthly_revenue": 80_000.0,
            "daily_orders": 25,
            "avg_order_value": 120.0,
            "price_level": 1.0,  # multiplier; 1.0 = base price
            "customer_satisfaction": 0.60,
            "active_campaigns": 0,
            "elasticity": 0.70,  # demand sensitivity to price
            "market_context": {},
        }

    def get_valid_actions(self) -> List[str]:
        return [
            "change_price",
            "add_offer",
            "run_campaign",
            "launch_bundle",
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

        if action_type == "change_price":
            direction = str(parameters.get("direction", "up")).lower()
            pct = self._safe_int(
                parameters.get("pct"), default=10, minimum=1, maximum=30
            )
            if direction == "up":
                s["price_level"] *= 1 + pct / 100
                s["avg_order_value"] *= 1 + pct / 100
                # Demand drops proportional to elasticity
                order_drop = s["daily_orders"] * (pct / 100) * s["elasticity"]
                s["daily_orders"] = max(1, int(s["daily_orders"] - order_drop))
                if pct > 15:
                    s["customer_satisfaction"] = max(
                        0.0, s["customer_satisfaction"] - 0.08 * (pct / 15)
                    )
            else:
                s["price_level"] *= 1 - pct / 100
                s["avg_order_value"] *= 1 - pct / 100
                # Demand grows
                order_gain = s["daily_orders"] * (pct / 100) * s["elasticity"]
                s["daily_orders"] = int(s["daily_orders"] + order_gain)
                s["customer_satisfaction"] = min(1.0, s["customer_satisfaction"] + 0.03)
                if any(
                    token in season_signal
                    for token in ["festive", "wedding", "holiday"]
                ):
                    s["daily_orders"] += 1
            s["monthly_revenue"] = s["daily_orders"] * s["avg_order_value"] * 30

        elif action_type == "add_offer":
            discount_pct = self._safe_int(
                parameters.get("discount_pct"), default=15, minimum=5, maximum=30
            )
            # Orders up, but margin falls
            order_gain = s["daily_orders"] * (discount_pct / 100) * 0.8
            s["daily_orders"] = int(s["daily_orders"] + order_gain)
            # Revenue: more orders × lower AOV
            effective_aov = s["avg_order_value"] * (1 - discount_pct / 100)
            s["monthly_revenue"] = s["daily_orders"] * effective_aov * 30
            s["customer_satisfaction"] = min(1.0, s["customer_satisfaction"] + 0.04)

        elif action_type == "run_campaign":
            ctype = str(parameters.get("type", "social")).lower()
            budget = self._safe_int(
                parameters.get("budget"), default=3000, minimum=0, maximum=500_000
            )
            roi = {"social": 3.5, "email": 2.5, "local": 2.2}
            revenue_boost = budget * roi.get(ctype, 2.0)
            s["monthly_revenue"] = min(
                s["monthly_revenue"] + revenue_boost,
                s["monthly_revenue"] * 1.40,  # cap at 40% single-campaign gain
            )
            s["daily_orders"] = int(s["monthly_revenue"] / (s["avg_order_value"] * 30))
            s["active_campaigns"] += 1
            s["customer_satisfaction"] = min(1.0, s["customer_satisfaction"] + 0.02)

        elif action_type == "launch_bundle":
            bundle_price = float(parameters.get("bundle_price", 200.0))
            items = (
                parameters.get("items", [])
                if isinstance(parameters.get("items", []), list)
                else []
            )
            # Bundle increases AOV if bundle_price > current AOV
            if bundle_price > s["avg_order_value"]:
                aov_lift = (bundle_price - s["avg_order_value"]) * 0.30
                s["avg_order_value"] += aov_lift
                order_gain = max(1, int(len(items) * 2))
                s["daily_orders"] += order_gain
                s["monthly_revenue"] = s["daily_orders"] * s["avg_order_value"] * 30
                s["customer_satisfaction"] = min(1.0, s["customer_satisfaction"] + 0.03)

        elif action_type == "no_op":
            pass

        goal_reached = (
            s["monthly_revenue"] >= self.TARGET_REVENUE
            and s["customer_satisfaction"] >= self.TARGET_SATISFACTION
        )
        return s, goal_reached

    def _safe_int(self, value: Any, default: int, minimum: int, maximum: int) -> int:
        try:
            parsed = int(value)
        except Exception:
            parsed = default
        return max(minimum, min(maximum, parsed))

    def grade(self, state: Dict[str, Any], steps_used: int) -> float:
        revenue_score = min(
            1.0,
            (state.get("monthly_revenue", 80_000.0) - 80_000)
            / (self.TARGET_REVENUE - 80_000),
        )
        satisfaction_score = min(1.0, state.get("customer_satisfaction", 0.0))
        order_score = min(1.0, (state.get("daily_orders", 25) - 25) / 15)
        efficiency_score = max(0.0, 1.0 - steps_used / self.MAX_STEPS)
        return round(
            0.50 * max(0.0, revenue_score)
            + 0.30 * satisfaction_score
            + 0.20 * max(0.0, order_score),
            4,
        )
