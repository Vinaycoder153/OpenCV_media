"""Pydantic v2 schemas for the OpenEnv Business Growth environment."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """All valid action types across all tasks."""

    # Task 1 – Social Media Growth
    GENERATE_POST = "generate_post"
    ADD_HASHTAGS = "add_hashtags"
    SCHEDULE_POST = "schedule_post"
    RUN_AD = "run_ad"

    # Task 2 – Review Management
    REPLY_REVIEW = "reply_review"
    REQUEST_REVIEW = "request_review"
    OFFER_DISCOUNT = "offer_discount"
    IMPROVE_SERVICE = "improve_service"

    # Task 3 – Revenue Optimization
    CHANGE_PRICE = "change_price"
    ADD_OFFER = "add_offer"
    RUN_CAMPAIGN = "run_campaign"
    LAUNCH_BUNDLE = "launch_bundle"

    # Generic
    NO_OP = "no_op"


class Action(BaseModel):
    """A structured action taken by the agent."""

    action_type: ActionType
    parameters: Dict[str, Any] = Field(default_factory=dict)


class BusinessMetrics(BaseModel):
    """Snapshot of key business metrics visible in every observation."""

    # Social media
    followers: int = 0
    engagement_rate: float = 0.0
    # Reviews
    avg_rating: float = 0.0
    total_reviews: int = 0
    positive_reviews: int = 0
    # Revenue
    monthly_revenue: float = 0.0
    daily_orders: int = 0
    avg_order_value: float = 0.0


class MarketContext(BaseModel):
    """Local market and seasonal signals attached to an episode."""

    city_tier: str = "unknown"
    season_signal: str = ""
    priority_channels: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)


class BusinessProfile(BaseModel):
    """Business identity used to personalise observations and rewards."""

    business_type: str = "business"
    location: str = "India"
    audience: str = ""
    budget_band: str = "standard"
    pricing_position: str = "mid-market"


class Observation(BaseModel):
    """Everything the agent sees at each step."""

    task_id: int
    step: int
    metrics: BusinessMetrics
    recent_actions: List[str] = Field(default_factory=list)
    trend: str = "stable"
    task_description: str = ""
    valid_actions: List[str] = Field(default_factory=list)
    hint: Optional[str] = None
    business_profile: Optional[BusinessProfile] = None
    market_context: Optional[MarketContext] = None


class Reward(BaseModel):
    """Reward signal returned after each step."""

    value: float
    components: Dict[str, float] = Field(default_factory=dict)
    reason: str = ""
    terminal_bonus: float = 0.0


class StepResult(BaseModel):
    """Full result returned by BusinessEnv.step()."""

    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)
