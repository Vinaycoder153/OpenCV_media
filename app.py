#!/usr/bin/env python3
"""FastAPI backend for AI Business Growth Agent.

Serves the React dashboard static files and exposes all /api/* endpoints.
Designed for Hugging Face Spaces (Docker SDK) on port 7860.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("app")

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="AI Business Growth Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Agent helpers
# ---------------------------------------------------------------------------

_agent_instance = None


def _get_agent():
    """Return a cached BusinessGrowthAgent, or None if no API key is set."""
    global _agent_instance  # noqa: PLW0603
    if _agent_instance is not None:
        return _agent_instance

    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        from agent.business_agent import BusinessGrowthAgent  # noqa: PLC0415

        _agent_instance = BusinessGrowthAgent(api_key=api_key)
        log.info("BusinessGrowthAgent initialized with LLM support.")
        return _agent_instance
    except Exception as exc:
        log.warning("Failed to initialize BusinessGrowthAgent: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Pydantic request/response models
# ---------------------------------------------------------------------------


class ContentGenerateRequest(BaseModel):
    businessType: str = "cafe"
    audience: str = "customers"
    tone: str = "friendly"


class ReviewItem(BaseModel):
    id: str
    author: str
    location: str
    rating: int
    sentiment: str
    review: str
    reply: str = ""


class ReviewAnalyzeRequest(BaseModel):
    reviews: List[ReviewItem]


class AssistantRequest(BaseModel):
    problem: str


class AutoModeRequest(BaseModel):
    days: Optional[int] = 14


# ---------------------------------------------------------------------------
# Mock / fallback helpers
# ---------------------------------------------------------------------------

_MOCK_SNAPSHOT: Dict[str, Any] = {
    "kpis": [
        {"label": "Monthly Revenue", "value": "₹12.4L", "change": "+18.2%", "trend": "up", "hint": "vs last 30 days"},
        {"label": "Engagement Rate", "value": "7.8%", "change": "+1.4 pts", "trend": "up", "hint": "social growth momentum"},
        {"label": "Average Rating", "value": "4.6", "change": "+0.3", "trend": "up", "hint": "review quality improving"},
        {"label": "AI Actions Completed", "value": "36", "change": "92% on-time", "trend": "flat", "hint": "planned tasks executed"},
    ],
    "trend": [
        {"label": "Mon", "revenue": 32000, "engagement": 4.2, "rating": 4.1, "orders": 84},
        {"label": "Tue", "revenue": 38400, "engagement": 4.9, "rating": 4.2, "orders": 92},
        {"label": "Wed", "revenue": 41800, "engagement": 5.4, "rating": 4.4, "orders": 105},
        {"label": "Thu", "revenue": 46600, "engagement": 6.1, "rating": 4.5, "orders": 117},
        {"label": "Fri", "revenue": 52100, "engagement": 6.9, "rating": 4.6, "orders": 128},
        {"label": "Sat", "revenue": 58300, "engagement": 7.4, "rating": 4.7, "orders": 142},
        {"label": "Sun", "revenue": 61200, "engagement": 7.8, "rating": 4.6, "orders": 137},
    ],
    "comparison": [
        {"label": "Posts Published", "value": 24},
        {"label": "Reviews Replied", "value": 18},
        {"label": "Campaign Reach", "value": 86},
        {"label": "Repeat Orders", "value": 64},
    ],
    "plan": [
        {"title": "Launch a morning reel for peak audience", "owner": "AI Growth Copilot", "duration": "15 min", "status": "running", "impact": "+12% engagement"},
        {"title": "Reply to 6 high-intent reviews", "owner": "Review Analyzer", "duration": "20 min", "status": "ready", "impact": "+0.2 rating lift"},
        {"title": "Push weekend bundle offer", "owner": "Revenue Engine", "duration": "30 min", "status": "queued", "impact": "+₹18K projected"},
    ],
    "quickActions": [
        {"title": "Generate post", "description": "Create a polished promo post in one click", "icon": "sparkles"},
        {"title": "Analyze reviews", "description": "Summarize sentiment and draft replies", "icon": "message-square-more"},
        {"title": "Build weekly report", "description": "See growth, risk, and next-best actions", "icon": "chart-column"},
    ],
    "assistantMessages": [
        {"id": "u-1", "role": "user", "content": "How do I increase revenue this week without increasing ad spend?", "timestamp": "Now"},
        {"id": "a-1", "role": "assistant", "content": "Focus on conversion efficiency before spending more.", "bullets": ["Bundle high-margin items with a time-bound offer.", "Shift social posts to the highest-performing audience slot.", "Reply to 5 recent reviews to strengthen purchase confidence."], "timestamp": "Just now"},
    ],
    "contentResult": {
        "post": "Morning ritual, upgraded. Fresh coffee, calm music, and a workspace designed for people who move fast. Today only: order your favorite combo and get 15% off before noon.",
        "caption": "Your weekday reset starts here. Come in for the coffee, stay for the vibe. #AIBusinessGrowth #SmallBusiness #GrowthMode",
        "hashtags": ["#AIBusinessGrowth", "#SmallBusiness", "#GrowthMode", "#CafeMarketing", "#LocalBusiness"],
        "reelIdea": "15-second before/after reel showing the store opening, a signature drink pour, and a customer reaction with upbeat motion text.",
    },
    "reviews": [
        {"id": "r-1", "author": "Ananya S.", "location": "Bangalore", "rating": 5, "sentiment": "positive", "review": "The service was fast and the cappuccino was excellent. Loved the new seating area.", "reply": "Thanks, Ananya. We are glad you enjoyed the service and the new seating. See you again soon!"},
        {"id": "r-2", "author": "Rahul K.", "location": "Mumbai", "rating": 4, "sentiment": "positive", "review": "Great food, but the wait time was a little longer than expected.", "reply": "Thanks for the honest feedback, Rahul. We are improving service speed and appreciate your patience."},
        {"id": "r-3", "author": "Priya M.", "location": "Pune", "rating": 3, "sentiment": "neutral", "review": "Good ambience, but the dessert selection could be better.", "reply": "Thanks for sharing, Priya. We are expanding the dessert menu and would love another chance to impress you."},
    ],
    "weeklyReport": {
        "headline": "Growth is compounding across content, reviews, and repeat orders.",
        "summary": "Revenue climbed 18.2% week-over-week while engagement crossed the 7% threshold. The fastest lift came from bundled offers and faster review response times.",
        "score": 84,
        "suggestions": [
            "Double down on weekday morning posts when engagement spikes.",
            "Expand high-margin bundles for the Saturday traffic window.",
            "Reply to every negative review within 2 hours to protect rating velocity.",
        ],
    },
    "autoMode": {
        "mode": "rule+ai",
        "periodLabel": "14-day autonomous sprint",
        "summary": "AI auto mode increased revenue while protecting ratings by sequencing low-cost local campaigns, review recovery, and offer optimization.",
        "impact": [
            {"key": "revenue", "label": "Monthly Revenue", "before": 1040000, "after": 1240000, "unit": "INR"},
            {"key": "engagement", "label": "Engagement Rate", "before": 6.2, "after": 7.8, "unit": "%"},
            {"key": "rating", "label": "Average Rating", "before": 4.3, "after": 4.6, "unit": "/5"},
            {"key": "orders", "label": "Daily Orders", "before": 109, "after": 137, "unit": "count"},
        ],
        "decisions": [
            {"step": 1, "dayLabel": "Day 1", "action": "Localized breakfast reel + 3km radius offer push", "rationale": "Morning conversion was strong but underexposed among office commuters.", "expectedImpact": "+8-10% walk-ins in weekday mornings", "actualImpact": "+9.2% morning footfall", "confidence": 0.88},
            {"step": 2, "dayLabel": "Day 4", "action": "Negative-review fast-response playbook with owner escalation", "rationale": "Sentiment dip around service-speed mentions was reducing map conversion.", "expectedImpact": "+0.15 rating recovery and lower churn risk", "actualImpact": "+0.18 rating recovery", "confidence": 0.91},
            {"step": 3, "dayLabel": "Day 9", "action": "Festival-lite combo bundle with premium add-on", "rationale": "AOV could be lifted without discounting core menu heavily.", "expectedImpact": "+11-14% AOV uplift", "actualImpact": "+12.6% AOV uplift", "confidence": 0.86},
        ],
    },
}


def _mock_content(business_type: str, audience: str, tone: str) -> Dict[str, Any]:
    bt = business_type.lower()
    return {
        "post": f"A better {bt} experience starts with knowing what {audience} actually care about. We built today's offer around speed, quality, and a smoother visit.",
        "caption": f"Built for {audience} who want a smarter {bt} moment. {'Premium service, clean execution.' if tone.lower() == 'premium' else 'Fast, simple, and designed to convert.'}",
        "hashtags": [f"#AIBusinessGrowth", "#SaaSStartup", "#SmallBusiness", f"#{bt.replace(' ', '')}", "#LocalBusiness"],
        "reelIdea": f"Show a {bt} transformation in 3 scenes: before, process, and the customer reaction. Close with a strong CTA for {audience}.",
    }


def _mock_assistant(problem: str) -> Dict[str, Any]:
    normalized = problem.lower()
    is_review = "review" in normalized or "rating" in normalized
    is_content = "post" in normalized or "content" in normalized or "social" in normalized
    is_revenue = "revenue" in normalized or "sales" in normalized or "orders" in normalized

    if is_review:
        bullets = [
            "Respond to recent negative reviews first to protect public perception.",
            "Use one clear service recovery template, then personalize each reply.",
            "Follow up with satisfied customers for fresh positive ratings.",
        ]
    elif is_content:
        bullets = [
            "Lead with one sharp value proposition in the first line.",
            "Use a clear offer, a visible deadline, and a specific CTA.",
            "Mix proof content with lifestyle content to avoid fatigue.",
        ]
    elif is_revenue:
        bullets = [
            "Increase average order value through bundles before increasing spend.",
            "Shift promotions to the highest-converting time windows.",
            "Protect margin by pairing a premium upsell with every campaign.",
        ]
    else:
        bullets = [
            "Clarify the one metric that matters most this week.",
            "Pick one high-leverage action and execute it consistently.",
            "Review the outcome after 48 hours and adjust fast.",
        ]

    return {
        "id": f"a-{int(time.time()*1000)}",
        "role": "assistant",
        "content": f"I analyzed your problem: {problem}. The fastest path is to focus on leverage, not more activity.",
        "bullets": bullets,
        "timestamp": "Just now",
    }


def _mock_auto_mode(days: int = 14) -> Dict[str, Any]:
    aggressiveness = min(1.35, max(0.8, days / 14))
    impact = []
    for m in _MOCK_SNAPSHOT["autoMode"]["impact"]:
        delta_map = {"revenue": 0.06, "engagement": 0.09, "rating": 0.05, "orders": 0.08}
        scale = delta_map.get(m["key"], 0.07) * aggressiveness
        after = min(5, m["before"] * (1 + scale)) if m["key"] == "rating" else m["before"] * (1 + scale)
        impact.append({**m, "after": round(after, 2 if m["key"] == "rating" else 0)})
    decisions = [
        {**d, "dayLabel": f"Day {min(days, (i + 1) * max(1, days // 3))}"}
        for i, d in enumerate(_MOCK_SNAPSHOT["autoMode"]["decisions"])
    ]
    return {
        "mode": "rule+ai",
        "periodLabel": f"{days}-day autonomous sprint",
        "summary": f"Autonomous mode executed {len(decisions)} high-leverage actions using rule checks + AI reasoning and produced measurable KPI lift.",
        "impact": impact,
        "decisions": decisions,
    }


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------


@app.get("/api/dashboard")
async def get_dashboard() -> Dict[str, Any]:
    return _MOCK_SNAPSHOT


@app.post("/api/content/generate")
async def generate_content(req: ContentGenerateRequest) -> Dict[str, Any]:
    agent = _get_agent()
    if agent is not None:
        try:
            text = agent.social_media_content(
                business_type=req.businessType,
                location="India",
                target_audience=req.audience,
                tone=req.tone,
                num_posts=1,
            )
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            hashtags = [w for line in lines for w in line.split() if w.startswith("#")]
            post = lines[0] if lines else text
            caption = lines[1] if len(lines) > 1 else post
            return {
                "post": post,
                "caption": caption,
                "hashtags": hashtags[:10] or _mock_content(req.businessType, req.audience, req.tone)["hashtags"],
                "reelIdea": lines[-1] if len(lines) > 2 else f"Short reel showcasing {req.businessType} for {req.audience}.",
            }
        except Exception as exc:
            log.warning("Agent content generation failed: %s", exc)
    return _mock_content(req.businessType, req.audience, req.tone)


@app.post("/api/reviews/analyze")
async def analyze_reviews(req: ReviewAnalyzeRequest) -> List[Dict[str, Any]]:
    agent = _get_agent()
    review_texts = [r.review for r in req.reviews]

    if agent is not None:
        try:
            agent.analyze_reviews(
                business_type="business",
                location="India",
                reviews=review_texts,
            )
        except Exception as exc:
            log.warning("Agent review analysis failed: %s", exc)

    result = []
    for r in req.reviews:
        if r.sentiment == "negative":
            reply = f"Thanks for the feedback, {r.author.split()[0]}. We are sorry the experience missed the mark and will address this right away."
        else:
            reply = r.reply or f"Thanks, {r.author.split()[0]}. We appreciate your support and look forward to welcoming you again."
        result.append({**r.model_dump(), "reply": reply})
    return result


@app.post("/api/assistant")
async def ask_assistant(req: AssistantRequest) -> Dict[str, Any]:
    agent = _get_agent()
    if agent is not None:
        try:
            text = agent.solve_business_problem(
                problem=req.problem,
                details="India-based small business",
            )
            lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("-")]
            bullets_raw = [l.lstrip("•·*-– ").strip() for l in text.splitlines() if l.strip().startswith(("-", "•", "·", "*"))]
            return {
                "id": f"a-{int(time.time()*1000)}",
                "role": "assistant",
                "content": lines[0] if lines else text[:200],
                "bullets": bullets_raw[:5] or None,
                "timestamp": "Just now",
            }
        except Exception as exc:
            log.warning("Agent assistant failed: %s", exc)
    return _mock_assistant(req.problem)


@app.get("/api/reports/weekly")
async def get_weekly_report() -> Dict[str, Any]:
    return _MOCK_SNAPSHOT["weeklyReport"]


@app.post("/api/auto-mode/run")
async def run_auto_mode(req: AutoModeRequest) -> Dict[str, Any]:
    days = max(3, min(30, req.days or 14))
    try:
        from agent.autonomous_mode import AutonomousGrowthRunner  # noqa: PLC0415

        runner = AutonomousGrowthRunner(seed=42)
        raw = runner.run(days=days)
        impact_list = []
        for task_id, task_data in raw.get("impact", {}).items():
            before = task_data.get("before", {})
            after = task_data.get("after", {})
            key_map = {
                "monthly_revenue": ("revenue", "Monthly Revenue", "INR"),
                "engagement_rate": ("engagement", "Engagement Rate", "%"),
                "avg_rating": ("rating", "Average Rating", "/5"),
                "daily_orders": ("orders", "Daily Orders", "count"),
            }
            for field, (key, label, unit) in key_map.items():
                if field in before and field in after:
                    impact_list.append({"key": key, "label": label, "before": round(before[field], 2), "after": round(after[field], 2), "unit": unit})
            break  # use task 3 for revenue-focused metrics

        decisions_raw = raw.get("decisions", [])
        decisions = [
            {
                "step": i + 1,
                "dayLabel": f"Day {d.get('day', i + 1)}",
                "action": d.get("action", ""),
                "rationale": d.get("rationale", ""),
                "expectedImpact": d.get("expected_outcome", ""),
                "actualImpact": f"reward: {d.get('reward', 0):.2f}",
                "confidence": min(0.99, 0.7 + d.get("reward", 0) * 0.05),
            }
            for i, d in enumerate(decisions_raw[:6])
        ]
        return {
            "mode": "rule+ai",
            "periodLabel": f"{days}-day autonomous sprint",
            "summary": raw.get("summary", ""),
            "impact": impact_list or _mock_auto_mode(days)["impact"],
            "decisions": decisions or _mock_auto_mode(days)["decisions"],
        }
    except Exception as exc:
        log.warning("AutonomousGrowthRunner failed: %s", exc)
    return _mock_auto_mode(days)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Serve React static files (must come last)
# ---------------------------------------------------------------------------

_STATIC_DIR = Path(__file__).parent / "dashboard-ui" / "dist"

if _STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(_STATIC_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = _STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(_STATIC_DIR / "index.html"))

else:
    log.warning("Static frontend not found at %s — UI will not be served.", _STATIC_DIR)

    @app.get("/")
    async def root():
        return {"message": "AI Business Growth Agent API is running. Frontend not built yet."}


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
