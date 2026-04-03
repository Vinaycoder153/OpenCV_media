# 🚀 AI Business Growth — OpenEnv Environment

A **production-ready reinforcement-learning environment** that simulates realistic
small-business operations (marketing, reviews, revenue) and exposes an OpenEnv-compliant
interface so AI agents can train, act, and be evaluated deterministically.

Designed for Indian small businesses (cafes, salons, restaurants, retail shops).

---

## 🌍 Real-World Relevance

India has 63+ million SMEs. Most lack data-driven tools to grow. This environment
simulates the exact growth levers available to a local business owner, making it ideal for:

- Training AI agents on realistic business strategy tasks
- Benchmarking LLM reasoning in structured decision environments
- Generating synthetic training data for downstream models

---

## 🏗️ Project Structure

```
opencv_pro/
├── env/                                  # OpenEnv environment
│   ├── __init__.py
│   ├── business_env.py                   # BusinessEnv: reset / step / state
│   ├── models/
│   │   └── schemas.py                    # Pydantic v2: Action, Observation, Reward …
│   ├── tasks/
│   │   ├── base_task.py
│   │   ├── task1_social_media.py         # Easy   (10 steps)
│   │   ├── task2_review_management.py    # Medium (12 steps)
│   │   └── task3_revenue_optimization.py # Hard   (15 steps)
│   └── graders/
│       ├── base_grader.py
│       ├── grader1.py                    # Social Media grader
│       ├── grader2.py                    # Review Management grader
│       └── grader3.py                    # Revenue grader
├── agent/
│   ├── __init__.py
│   ├── baseline_agent.py                 # Heuristic + GPT-4o-mini agent
│   ├── action_parser.py                  # LLM text → Action, per-task prompts
│   ├── business_agent.py                 # Interactive CLI agent
│   ├── prompts.py
│   └── capabilities/                     # 9 advisory capabilities
├── config/
│   └── openenv.yaml                      # Task targets, model, logging
├── deployment/
│   └── Dockerfile                        # python:3.11-slim container
├── tests/
│   └── test_agent.py
├── main.py                               # Interactive CLI entry point
├── requirements.txt
└── README.md
```

---

## 🎯 Task Descriptions

### Task 1 — Social Media Growth (Easy)

| Parameter | Value |
|-----------|-------|
| Max steps | 10 |
| Starting state | 500 followers, 2% engagement |
| Goal | ≥ 1 000 followers AND ≥ 5% engagement rate |

**Available actions:** `generate_post`, `add_hashtags`, `schedule_post`, `run_ad`, `no_op`

### Task 2 — Review Management (Medium)

| Parameter | Value |
|-----------|-------|
| Max steps | 12 |
| Starting state | avg_rating 3.2, sentiment 0.40 |
| Goal | avg_rating ≥ 4.0 AND sentiment_score ≥ 0.7 |

**Available actions:** `reply_review`, `request_review`, `offer_discount`, `improve_service`, `no_op`

### Task 3 — Revenue Optimization (Hard)

| Parameter | Value |
|-----------|-------|
| Max steps | 15 |
| Starting state | ₹80,000/month revenue, 25 daily orders |
| Goal | ≥ ₹1,20,000/month AND customer_satisfaction ≥ 0.7 |

**Available actions:** `change_price`, `add_offer`, `run_campaign`, `launch_bundle`, `no_op`

---

## 🎮 Action Space

Each action is a JSON object with `action_type` and `parameters`:

```json
{"action_type": "generate_post",  "parameters": {"quality": 4}}
{"action_type": "reply_review",   "parameters": {"tone": "professional"}}
{"action_type": "run_campaign",   "parameters": {"type": "social", "budget": 5000}}
{"action_type": "launch_bundle",  "parameters": {"items": ["coffee", "cake"], "bundle_price": 180.0}}
```

Invalid / repeated actions are penalised; destructive decisions reduce rewards.

---

## 📊 Observation Space

```json
{
  "task_id": 1,
  "step": 3,
  "metrics": {
    "followers": 720,
    "engagement_rate": 0.038,
    "avg_rating": 0.0,
    "monthly_revenue": 0.0
  },
  "recent_actions": ["add_hashtags", "schedule_post", "generate_post"],
  "trend": "growing",
  "task_description": "Grow followers to 1000+ ...",
  "valid_actions": ["generate_post", "add_hashtags", "schedule_post", "run_ad", "no_op"]
}
```

---

## 🎁 Reward Design

The reward is **continuous and shaped** across steps:

| Component | When | Value |
|-----------|------|-------|
| `progress` | Positive metric delta | +0.4 – +0.6 × normalised delta |
| `no_op_penalty` | `no_op` action | −0.10 |
| `spam_penalty` | Same action 3+ times in a row | −0.05 × (run − 1) |
| `destructive` | Large negative metric change | proportional negative |
| `goal_bonus` | Goal reached | +1.0 |

---

## 🧠 Grader System

Each grader returns a score in [0.0, 1.0]:

| Label | Range |
|-------|-------|
| Poor | < 0.4 |
| Average | 0.4 – 0.7 |
| Good | > 0.7 |

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your OpenAI API key (optional)

```bash
export OPENAI_API_KEY="sk-..."
```

If the key is not set, the baseline agent automatically runs in **heuristic mode** —
no API calls required.

---

## 🤖 Run the Baseline Agent

```bash
python agent/baseline_agent.py
```

Example output:

```
08:15:57 [INFO] === AI Business Growth Baseline Agent ===
08:15:57 [INFO] Mode: Heuristic (no API key)

--- Task 1 ---
08:15:57 [INFO] Step  1 | action=add_hashtags          | reward=+0.000 | done=False
08:15:57 [INFO] Step  3 | action=generate_post         | reward=+0.544 | done=False
08:15:57 [INFO] Step  9 | action=run_ad                | reward=+1.400 | done=True

============================================================
Task     Steps    Score       Goal        Total Reward
------------------------------------------------------------
Task 1    9        0.8200      ✓           +3.5310
Task 2    12       0.5491      ✗           +0.8663
Task 3    4        0.7663      ✓           +2.4175
============================================================
```

---

## 🐍 Use the Environment Directly

```python
from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType

# Task 1: Social Media Growth
env = BusinessEnv(task_id=1, seed=42)
obs = env.reset()
print(obs.metrics)          # followers=500, engagement_rate=0.02

action = Action(action_type=ActionType.GENERATE_POST, parameters={"quality": 5})
result = env.step(action)
print(result.reward.value)  # positive progress reward
print(result.observation.metrics.followers)  # followers increased

# Check full state
state = env.state()
print(state["task_state"])
```

---

## 🖥️ Run the Interactive CLI Agent

```bash
python main.py
```

---

## 🧪 Run Tests

```bash
python -m pytest tests/ -v
```

Tests use `unittest.mock` — no real API calls, no API key needed.

---

## 🐳 Docker

```bash
# Build
docker build -f deployment/Dockerfile -t ai-business-growth .

# Run (heuristic mode, no API key needed)
docker run ai-business-growth

# Run with LLM mode
docker run -e OPENAI_API_KEY=sk-... ai-business-growth
```

---

## 📋 Baseline Results (Heuristic Agent)

| Task | Difficulty | Max Steps | Score | Goal Reached |
|------|-----------|-----------|-------|-------------|
| Social Media Growth | Easy | 10 | ~0.82 | ✓ |
| Review Management | Medium | 12 | ~0.55 | ✗ |
| Revenue Optimization | Hard | 15 | ~0.77 | ✓ |

---

## 🔑 Configuration

Edit `config/openenv.yaml` to customise task targets, model, and logging:

```yaml
tasks:
  task1:
    target:
      followers: 1000
      engagement_rate: 0.05
agent:
  model: "gpt-4o-mini"
  temperature: 0.0
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `openai>=1.30.0` | LLM agent mode |
| `pydantic>=2.0.0` | Typed schemas (Action, Observation, Reward) |
| `pyyaml>=6.0` | Config loading |
| `pytest>=7.0.0` | Testing |
