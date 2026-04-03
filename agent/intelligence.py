"""Shared product-intelligence helpers for the AI Business Growth platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable, List, Optional


_METRO_CITIES = {
    "bangalore",
    "bengaluru",
    "mumbai",
    "delhi",
    "new delhi",
    "gurugram",
    "gurgaon",
    "hyderabad",
    "chennai",
    "kolkata",
    "pune",
    "ahmedabad",
    "noida",
}


@dataclass(frozen=True)
class BusinessContext:
    business_type: str
    location: str
    audience: str = ""
    budget: int = 0
    revenue: int = 0
    focus_area: str = ""
    problem: str = ""

    @property
    def city_tier(self) -> str:
        city = self.location.lower().strip()
        if any(name in city for name in _METRO_CITIES):
            return "metro"
        if city:
            return "tier-2/3"
        return "unknown"

    @property
    def season_signal(self) -> str:
        today = date.today()
        month = today.month
        if month in {1, 2}:
            return "new-year momentum, weddings, gifting"
        if month in {3, 4}:
            return "summer prep, exam season, local weekend traffic"
        if month in {5, 6}:
            return "summer hydration, cooling offers, indoor experiences"
        if month in {7, 8}:
            return "monsoon convenience, comfort menus, back-to-school demand"
        if month in {9, 10}:
            return "festive pre-heat, Navratri, Dussehra, premium upsells"
        if month in {11}:
            return "Diwali recovery, gifting, retention campaigns"
        return "holiday gifting, recap campaigns, year-end retention"

    @property
    def channel_priority(self) -> List[str]:
        business = self.business_type.lower()
        audience = self.audience.lower()
        channels: List[str] = ["Instagram", "WhatsApp", "Google Business Profile"]
        if any(word in business for word in ["cafe", "restaurant", "food", "bakery"]):
            channels.insert(0, "Google Maps")
        if any(word in business for word in ["salon", "spa", "clinic"]):
            channels.insert(0, "WhatsApp Business")
        if any(word in audience for word in ["college", "student", "gen z"]):
            channels.insert(0, "Reels")
        return channels[:4]

    @property
    def risk_flags(self) -> List[str]:
        flags: List[str] = []
        if self.budget and self.budget < 1000:
            flags.append("tight-budget")
        if self.revenue and self.revenue < 50000:
            flags.append("low-cash-buffer")
        if self.city_tier == "tier-2/3":
            flags.append("local-trust-dependency")
        return flags


def build_business_context(
    business_type: str,
    location: str,
    audience: str = "",
    budget: int = 0,
    revenue: int = 0,
    focus_area: str = "",
    problem: str = "",
) -> BusinessContext:
    return BusinessContext(
        business_type=business_type.strip() or "business",
        location=location.strip() or "India",
        audience=audience.strip(),
        budget=max(0, int(budget or 0)),
        revenue=max(0, int(revenue or 0)),
        focus_area=focus_area.strip(),
        problem=problem.strip(),
    )


def build_context_brief(context: BusinessContext) -> str:
    signals = ", ".join(context.channel_priority)
    risks = ", ".join(context.risk_flags) if context.risk_flags else "none"
    return (
        "Operating context:\n"
        f"- Business type: {context.business_type}\n"
        f"- Location: {context.location}\n"
        f"- City tier: {context.city_tier}\n"
        f"- Audience: {context.audience or 'not specified'}\n"
        f"- Revenue band: ₹{context.revenue:,} / month\n"
        f"- Budget available: ₹{context.budget:,}\n"
        f"- Focus area: {context.focus_area or 'general growth'}\n"
        f"- Problem statement: {context.problem or 'not specified'}\n"
        f"- Seasonal / market signal: {context.season_signal}\n"
        f"- Priority channels: {signals}\n"
        f"- Risk flags: {risks}\n"
        "Instructions:\n"
        "- Recommend actions that can be executed by a small Indian business owner.\n"
        "- Avoid generic marketing advice and non-actionable fluff.\n"
        "- Prefer low-cost, measurable, high-leverage moves.\n"
        "- Include the local timing angle, festival relevance, or seasonality when useful."
    )


def build_fallback_response(prompt: str, context_brief: str = "") -> str:
    prompt_lower = prompt.lower()
    sections = [
        "📌 Executive Summary",
        "The system is using a safe offline fallback. Focus on one concrete move, then measure the result within 24-48 hours.",
        "🎯 Priority Action",
        "Use the strongest channel for the business, keep the offer simple, and tie the message to local buying intent.",
        "🚀 Quick Win",
        "Publish one targeted update today with a clear CTA, proof point, and time-bound offer.",
        "⚠️ Risk to Avoid",
        "Do not add more actions without checking conversion, reviews, or response rate first.",
    ]

    if any(keyword in prompt_lower for keyword in ["review", "rating", "sentiment"]):
        sections[1] = (
            "Respond to the top complaint first, use a calm recovery tone, and close the loop publicly when appropriate."
        )
    elif any(
        keyword in prompt_lower for keyword in ["revenue", "price", "bundle", "offer"]
    ):
        sections[1] = (
            "Protect margin, raise average order value, and use bundles or timed offers before increasing spend."
        )
    elif any(
        keyword in prompt_lower
        for keyword in ["post", "social", "instagram", "content"]
    ):
        sections[1] = (
            "Lead with one clear promise, one proof point, and one action the audience can take right now."
        )

    if context_brief:
        sections.insert(2, "📍 Context Signal")
        sections.insert(3, context_brief)

    return "\n".join(sections)
