#!/usr/bin/env python3
"""
Business Growth Agent — interactive CLI.

Usage
-----
    python main.py

Set your Google API key before running:

    export OPENAI_API_KEY="..."
"""

from __future__ import annotations

import sys
from typing import Optional

from agent import BusinessGrowthAgent

# Default hours available for growth tasks in the daily action planner
_DEFAULT_GROWTH_HOURS = 8.0
from openai import OpenAI

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _separator(char: str = "─", width: int = 60) -> str:
    return char * width


def _prompt(label: str, default: Optional[str] = None) -> str:
    """Read a non-empty string from stdin, using default when supplied."""
    suffix = f" [{default}]" if default else ""
    while True:
        value = input(f"  {label}{suffix}: ").strip()
        if value:
            return value
        if default is not None:
            return default
        print("  ⚠️  This field is required. Please enter a value.")


def _prompt_int(label: str, default: int = 0) -> int:
    while True:
        raw = input(f"  {label} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  ⚠️  Please enter a whole number.")


def _prompt_float(label: str, default: float = 8.0) -> float:
    while True:
        raw = input(f"  {label} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  ⚠️  Please enter a number (e.g. 4 or 1.5).")


# ---------------------------------------------------------------------------
# Menu handlers
# ---------------------------------------------------------------------------


def _social_media(agent: BusinessGrowthAgent) -> None:
    print("\n📱 Social Media Content Generator")
    print(_separator())
    btype = _prompt("Business type (e.g. cafe, salon)")
    loc = _prompt("Location (e.g. Koramangala, Bangalore)")
    audience = _prompt("Target audience (e.g. college students, working women)")
    platform = _prompt("Platform", "Instagram")
    theme = _prompt("Theme / occasion", "general promotion")
    tone = _prompt("Tone", "friendly and engaging")
    num = _prompt_int("Number of posts to generate (1-5)", 3)

    print("\n⏳ Generating content...\n")
    result = agent.social_media_content(
        business_type=btype,
        location=loc,
        target_audience=audience,
        platform=platform,
        theme=theme,
        tone=tone,
        num_posts=num,
    )
    print(result)


def _growth_strategy(agent: BusinessGrowthAgent) -> None:
    print("\n📈 Growth Strategy Advisor")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    problem = _prompt("Main business problem / challenge")
    revenue = _prompt_int("Current monthly revenue in ₹ (0 if unknown)", 0)
    budget = _prompt_int("Monthly marketing budget in ₹ (0 if unknown)", 0)

    print("\n⏳ Analysing...\n")
    result = agent.growth_strategy(
        business_type=btype,
        location=loc,
        problem=problem,
        monthly_revenue=revenue,
        marketing_budget=budget,
    )
    print(result)


def _review_analysis(agent: BusinessGrowthAgent) -> None:
    print("\n⭐ Review Analyser")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    print("  Paste your customer reviews below.")
    print("  Enter each review on a new line.")
    print("  Type 'DONE' on its own line when finished.\n")
    lines = []
    while True:
        line = input("  > ")
        if line.strip().upper() == "DONE":
            break
        lines.append(line)

    print("\n⏳ Analysing reviews...\n")
    result = agent.analyze_reviews(
        business_type=btype,
        location=loc,
        reviews=lines,
    )
    print(result)


def _performance_report(agent: BusinessGrowthAgent) -> None:
    print("\n📊 Weekly Performance Report")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    footfall = _prompt_int("This week's footfall / orders", 0)
    revenue = _prompt_int("This week's revenue in ₹", 0)
    new_cust = _prompt_int("New customers this week", 0)
    repeat_cust = _prompt_int("Repeat customers this week", 0)
    top_item = _prompt("Top-selling item / service this week")
    social_reach = _prompt_int("Social media reach / impressions (0 if unknown)", 0)

    print("\n⏳ Building report...\n")
    result = agent.performance_report(
        business_type=btype,
        location=loc,
        footfall=footfall,
        revenue=revenue,
        new_customers=new_cust,
        repeat_customers=repeat_cust,
        top_item=top_item,
        social_reach=social_reach,
    )
    print(result)


def _customer_personas(agent: BusinessGrowthAgent) -> None:
    print("\n👥 Customer Persona Generator")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    avg_txn = _prompt_int("Average transaction value in ₹", 200)
    peak = _prompt("Peak hours (e.g. 12 PM – 2 PM and 7 PM – 9 PM)")
    obs = _prompt("Any observations about your customers? (press Enter to skip)", "")

    print("\n⏳ Generating personas...\n")
    result = agent.customer_personas(
        business_type=btype,
        location=loc,
        avg_transaction=avg_txn,
        peak_hours=peak,
        observations=obs,
    )
    print(result)


def _pricing_offers(agent: BusinessGrowthAgent) -> None:
    print("\n💰 Pricing & Offers Advisor")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    current = _prompt("Current pricing (brief description)")
    competitor = _prompt("Competitor pricing (press Enter if unknown)", "unknown")
    goal = _prompt("Your pricing goal (e.g. increase avg order value)")

    print("\n⏳ Building strategy...\n")
    result = agent.pricing_and_offers(
        business_type=btype,
        location=loc,
        current_pricing=current,
        goal=goal,
        competitor_pricing=competitor,
    )
    print(result)


def _daily_plan(agent: BusinessGrowthAgent) -> None:
    print("\n📅 Daily Action Plan")
    print(_separator())
    btype = _prompt("Business type")
    loc = _prompt("Location")
    focus = _prompt("Today's focus area (e.g. social media, new offers, service speed)")
    hours = _prompt_float(
        "Hours available for growth tasks today", _DEFAULT_GROWTH_HOURS
    )
    budget = _prompt_int("Budget available today in ₹ (0 if none)", 0)

    print("\n⏳ Creating your plan...\n")
    result = agent.daily_action_plan(
        business_type=btype,
        location=loc,
        focus_area=focus,
        available_time=hours,
        budget=budget,
    )
    print(result)


def _instagram_content(agent: BusinessGrowthAgent) -> None:
    print("\n📸 Instagram Content Generator")
    print(_separator())
    btype = _prompt("Business type (e.g. cafe, salon, boutique)")
    loc = _prompt("Location (e.g. Koramangala, Bangalore)")
    audience = _prompt("Target audience (e.g. college students, working women)")

    print("\n⏳ Generating Instagram content...\n")
    result = agent.instagram_content(
        business_type=btype,
        location=loc,
        audience=audience,
    )
    print(result)


def _problem_solver(agent: BusinessGrowthAgent) -> None:
    print("\n🧩 Business Problem Solver")
    print(_separator())
    problem = _prompt("Describe your business problem")
    details = _prompt("Business details (type, location, budget, team size, etc.)")

    print("\n⏳ Analysing and generating solutions...\n")
    result = agent.solve_business_problem(
        problem=problem,
        details=details,
    )
    print(result)


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

MENU_OPTIONS = {
    "1": ("📱  Generate Social Media Content", _social_media),
    "2": ("📈  Get Growth Strategy", _growth_strategy),
    "3": ("⭐  Analyse Customer Reviews", _review_analysis),
    "4": ("📊  Generate Weekly Performance Report", _performance_report),
    "5": ("👥  Generate Customer Personas", _customer_personas),
    "6": ("💰  Pricing & Offers Advice", _pricing_offers),
    "7": ("📅  Create Daily Action Plan", _daily_plan),
    "8": ("📸  Generate Instagram Content Kit", _instagram_content),
    "9": ("🧩  Solve a Business Problem", _problem_solver),
    "0": ("🚪  Exit", None),
}


def main() -> None:
    print("\n" + "=" * 60)
    print("  🚀 AI Business Growth Agent — India Edition")
    print("=" * 60)
    print("  Your personal business growth partner.\n")

    try:
        agent = BusinessGrowthAgent()
    except ValueError as exc:
        print(f"\n❌ {exc}\n")
        sys.exit(1)

    while True:
        print("\n" + _separator())
        print("  What would you like to do?\n")
        for key, (label, _) in MENU_OPTIONS.items():
            print(f"  [{key}] {label}")
        print()

        choice = input("  Your choice: ").strip()

        if choice == "0":
            print("\n👋 See you next time! Keep growing! 🌱\n")
            break

        if choice not in MENU_OPTIONS:
            print("  ⚠️  Invalid option. Please enter a number from the menu.")
            continue

        _, handler = MENU_OPTIONS[choice]
        if handler:
            print()
            try:
                handler(agent)
            except KeyboardInterrupt:
                print("\n\n  (Cancelled — returning to menu)")
            except (ValueError, IOError) as exc:
                print(f"\n❌ An error occurred: {exc}")


if __name__ == "__main__":
    main()
