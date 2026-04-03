"""
Structured system and user prompts for each agent capability.

All prompts are designed to produce responses following the STRICT output format:
  - Section titles with emojis
  - Bullet points
  - Clear actionable steps
  - At least 1 "quick win"
  - At least 1 "mistake to avoid"
"""

# ---------------------------------------------------------------------------
# System prompt — shared across every capability
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an elite AI Business Growth Agent specialised in helping small and
local businesses (cafes, restaurants, salons, retail shops) in India grow
their revenue, customer engagement, and online presence.

Think like:
- A marketing strategist
- A customer psychology expert
- A data analyst
- A local business consultant

Response rules (STRICT):
- Use section titles with emojis
- Use bullet points throughout
- Keep language simple and owner-friendly (avoid jargon)
- Be specific and actionable — no generic advice
- Consider Indian festivals, culture, and regional trends
- Always include a "🚀 Quick Win" section with 1 action doable today
- Always include a "⚠️ Mistake to Avoid" section
- Prefer numbers, timelines, expected impact, and clear next steps
- Tie recommendations to the supplied business context and market signals
- Do not repeat the prompt or explain your reasoning process
- Never use filler phrases like "Great question!" or "As an AI..."
""".strip()

# ---------------------------------------------------------------------------
# Capability-specific user prompt templates
# ---------------------------------------------------------------------------
SOCIAL_MEDIA_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}
- Target audience: {target_audience}
- Platform: {platform}
- Theme / occasion: {theme}
- Tone: {tone}

Generate {num_posts} social media post(s) optimised for {platform}.
Each post must include:
1. Caption (engaging, platform-appropriate length)
2. Relevant hashtags (mix of trending + niche)
3. Best time to post
4. Content format suggestion (image / reel / carousel / story)
5. Local angle / festival / market trigger, when relevant
6. Direct CTA and one metric to watch
""".strip()

GROWTH_STRATEGY_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}
- Current monthly revenue: ₹{monthly_revenue}
- Main problem: {problem}
- Budget for marketing: ₹{marketing_budget}

Provide a growth strategy that directly solves the stated problem.
Include:
1. Root cause analysis of the problem
2. Top 3 prioritised action steps (with timeline: week 1 / month 1 / month 3)
3. Low-cost or free tactics that work in India
4. One referral or word-of-mouth idea
5. One metric per recommendation and a realistic expected impact range
""".strip()

REVIEW_ANALYSIS_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}

Customer reviews to analyse:
\"\"\"
{reviews}
\"\"\"

Provide:
1. Overall sentiment score (Positive / Neutral / Negative) with % breakdown
2. Top 3 things customers love
3. Top 3 pain points or complaints
4. Actionable improvements for each pain point
5. Suggested owner response template for a negative review
6. A prioritised 24-hour recovery plan
""".strip()

PERFORMANCE_REPORT_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}

Weekly metrics:
- Footfall / orders: {footfall}
- Revenue: ₹{revenue}
- New customers: {new_customers}
- Repeat customers: {repeat_customers}
- Top-selling item / service: {top_item}
- Social media reach: {social_reach}

Generate a weekly performance report with:
1. Key wins this week
2. Areas that need attention
3. Week-over-week trend insight (based on provided numbers)
4. 3 specific goals for next week
5. A scorecard the owner can review in 5 minutes
""".strip()

PERSONA_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}
- Average transaction value: ₹{avg_transaction}
- Peak hours: {peak_hours}
- Observations about customers: {observations}

Create 2 detailed customer personas. For each persona include:
1. Name, age, occupation, income bracket
2. Goals and motivations for visiting
3. Pain points or objections
4. Preferred communication channel (WhatsApp / Instagram / etc.)
5. Ideal offer or incentive to retain them
6. One local or seasonal trigger that increases conversion
""".strip()

PRICING_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}
- Current pricing: {current_pricing}
- Competitor pricing: {competitor_pricing}
- Goal: {goal}

Suggest a pricing and offers strategy that:
1. Maximises revenue per customer
2. Drives repeat visits
3. Uses psychological pricing techniques
4. Includes at least 1 bundle / combo offer idea
5. Recommends a loyalty or referral programme suited to India
6. States the risk of over-discounting and how to control it
""".strip()

INSTAGRAM_CONTENT_PROMPT = """
Business Details:
- Type: {business_type}
- Location: {location}
- Target Audience: {audience}

Generate Instagram content that is culturally relevant to Indian festivals and trends.
Tone: Friendly, modern, catchy.

Produce exactly the following sections (use these headings):

📸 Instagram Post
Write a short, engaging post (2-4 sentences) that grabs attention instantly.

✍️ Caption
Write one caption that combines emotion with a clear call-to-action.

#️⃣ Hashtags
List exactly 10 hashtags — mix local/city-specific tags with currently trending Indian tags.

🎬 Reel Idea
Describe one high-engagement Reel concept (hook, content flow, on-screen text/audio suggestions).
""".strip()

ACTION_PLAN_PROMPT = """
Business context:
- Type: {business_type}
- Location: {location}
- Focus area today: {focus_area}
- Available time: {available_time} hours
- Budget available: ₹{budget}

Create a practical daily action plan. Include:
1. Morning tasks (open / prep)
2. Customer-facing tasks during business hours
3. Marketing / social media tasks
4. Evening wrap-up and review tasks
5. One habit to build over the next 30 days
6. A time budget for each block and a single success metric
""".strip()

PROBLEM_SOLVER_PROMPT = """
Business Problem:
{problem}

Business Details:
{details}

Focus on low-budget, high-impact actions suited to small and local Indian businesses.

Produce exactly the following sections (use these headings):

💡 3 Actionable Strategies
List three specific, practical strategies that directly address the problem above.
For each strategy include a brief explanation and one concrete first step.

🚀 Quick Win
Describe one action the owner can take TODAY that will show visible results quickly.

📈 Long-Term Strategy
Describe one play that will compound over 3-6 months and build a sustainable advantage.

⚠️ Mistake to Avoid
Name one common mistake owners make when facing this problem and explain why it backfires.

📊 What to Measure
Add 2-3 KPIs that prove the strategy is working.
""".strip()
