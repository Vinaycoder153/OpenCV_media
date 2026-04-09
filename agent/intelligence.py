"""Shared product-intelligence helpers for the AI Business Growth platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Tuple


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

# Indian festival calendar — approximate dates (month, day) and marketing relevance
# Covers the full year so the system always has upcoming festival context.
_INDIAN_FESTIVALS: List[Dict] = [
    {"name": "Makar Sankranti", "month": 1, "day": 14, "boost": "sweets, til-gur, kite themes; family gifting window"},
    {"name": "Republic Day", "month": 1, "day": 26, "boost": "patriotic offers, early-morning footfall spike"},
    {"name": "Valentine's Day", "month": 2, "day": 14, "boost": "couple combos, dessert bundles, gifting push"},
    {"name": "Holi", "month": 3, "day": 25, "boost": "colour-themed menus, festive reels, family group visits"},
    {"name": "Gudi Padwa / Ugadi", "month": 3, "day": 30, "boost": "new-year offers, community events, sweet hampers"},
    {"name": "Ram Navami", "month": 4, "day": 6, "boost": "devotional audience, sattvic menu highlights"},
    {"name": "Eid ul-Fitr", "month": 4, "day": 10, "boost": "evening surge, halal offerings, family feasts, gift cards"},
    {"name": "Mother's Day", "month": 5, "day": 11, "boost": "family brunch, gifting combos, emotional storytelling"},
    {"name": "Eid al-Adha", "month": 6, "day": 17, "boost": "premium sharing platters, community dining"},
    {"name": "Independence Day", "month": 8, "day": 15, "boost": "tricolour specials, patriotic reels, morning rush"},
    {"name": "Janmashtami", "month": 8, "day": 16, "boost": "midnight snacks, dairy specials, festive decor reels"},
    {"name": "Ganesh Chaturthi", "month": 9, "day": 5, "boost": "modak combos, 10-day promotions, family offerings"},
    {"name": "Navratri", "month": 10, "day": 2, "boost": "fasting menus, garba nights, special dietary offers"},
    {"name": "Dussehra", "month": 10, "day": 12, "boost": "festive launch window, premium bundles, gifting"},
    {"name": "Diwali", "month": 10, "day": 20, "boost": "HIGHEST traffic week of year — gift hampers, premium offers, loyalty rewards"},
    {"name": "Bhai Dooj", "month": 10, "day": 22, "boost": "sibling combos, gifting push, sweet specials"},
    {"name": "Chhath Puja", "month": 10, "day": 28, "boost": "Bihar/UP audience, traditional items, community focus"},
    {"name": "Guru Nanak Jayanti", "month": 11, "day": 5, "boost": "Punjabi cuisine, community charity tie-ins"},
    {"name": "Christmas", "month": 12, "day": 25, "boost": "premium gifting, year-end celebration, party packages"},
    {"name": "New Year's Eve", "month": 12, "day": 31, "boost": "party packages, countdown offers, premium reservations"},
]


def get_upcoming_festivals(n: int = 3) -> List[Dict]:
    """Return the next *n* upcoming Indian festivals from today."""
    today = date.today()
    scored: List[Tuple[int, Dict]] = []
    for fest in _INDIAN_FESTIVALS:
        festival_date = date(today.year, fest["month"], fest["day"])
        if festival_date < today:
            # Use next year's date
            try:
                festival_date = date(today.year + 1, fest["month"], fest["day"])
            except ValueError:
                continue
        days_until = (festival_date - today).days
        scored.append((days_until, {**fest, "date": festival_date.isoformat(), "days_until": days_until}))
    scored.sort(key=lambda x: x[0])
    return [item for _, item in scored[:n]]


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
        upcoming = get_upcoming_festivals(1)
        festival_hint = ""
        if upcoming and upcoming[0]["days_until"] <= 14:
            festival_hint = f"; {upcoming[0]['name']} in {upcoming[0]['days_until']} days — {upcoming[0]['boost']}"
        if month in {1, 2}:
            return f"new-year momentum, weddings, gifting{festival_hint}"
        if month in {3, 4}:
            return f"summer prep, exam season, local weekend traffic{festival_hint}"
        if month in {5, 6}:
            return f"summer hydration, cooling offers, indoor experiences{festival_hint}"
        if month in {7, 8}:
            return f"monsoon convenience, comfort menus, back-to-school demand{festival_hint}"
        if month in {9, 10}:
            return f"festive pre-heat, Navratri, Dussehra, premium upsells{festival_hint}"
        if month in {11}:
            return f"Diwali recovery, gifting, retention campaigns{festival_hint}"
        return f"holiday gifting, recap campaigns, year-end retention{festival_hint}"

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
