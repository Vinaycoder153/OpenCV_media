# AI Business Growth OpenEnv Environment

Production-ready OpenEnv-style reinforcement learning environment for business growth decisions, optimized for deterministic evaluation and Hugging Face Spaces Docker deployment.

## What the environment does

The environment simulates small-business decision making across three tasks:

1. Social media growth
2. Review management
3. Revenue optimization

Each episode follows an OpenEnv-compatible loop:

- `obs = env.reset()`
- `result = env.step(action)`
- `state = env.state()`

The canonical hackathon entrypoint is `inference.py` at repository root.

## Tasks

### Task 1: Social Media Growth

- Max steps: `10`
- Initial state: `followers=500`, `engagement_rate=0.02`
- Goal: `followers >= 1000` and `engagement_rate >= 0.05`

### Task 2: Review Management

- Max steps: `12`
- Initial state: `avg_rating=3.2`, `sentiment_score=0.40`
- Goal: `avg_rating >= 4.0` and `sentiment_score >= 0.7`

### Task 3: Revenue Optimization

- Max steps: `15`
- Initial state: `monthly_revenue=80000`, `daily_orders=25`
- Goal: `monthly_revenue >= 120000` and `customer_satisfaction >= 0.7`

## Action space

Actions are JSON objects:

```json
{"action_type":"generate_post","parameters":{"quality":4}}
{"action_type":"reply_review","parameters":{"tone":"professional"}}
{"action_type":"run_campaign","parameters":{"type":"social","budget":4000}}
{"action_type":"launch_bundle","parameters":{"items":["coffee","snack"],"bundle_price":210.0}}
```

## Observation space

Observations expose task context, current metrics, and valid actions:

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
  "valid_actions": ["generate_post", "add_hashtags", "schedule_post", "run_ad", "no_op"]
}
```

## Reward design

Reward is shaped and continuous with additive components:

- Positive progress (`progress`)
- No-op penalty (`no_op_penalty`)
- Repetition penalty (`spam_penalty`)
- Destructive-change penalty (`destructive`)
- Goal/terminal bonus (`goal_bonus`, `terminal_bonus`)

Task graders map terminal performance to `[0.0, 1.0]`.

## Hackathon inference contract

`inference.py` guarantees:

- `API_BASE_URL` default: `https://api.openai.com/v1`
- `MODEL_NAME` default: `gpt-4o-mini`
- `HF_TOKEN` validation when `USE_LLM=true`
- OpenAI Python client usage only
- Output envelope in exact order:
  - `[START]`
  - repeated `[STEP]` + one-line JSON payload
  - `[END]`
- JSON booleans are lowercase (native JSON `true`/`false`)
- Reward values are emitted as strings formatted to exactly 2 decimals
- `[END]` is emitted even when exceptions occur

## Setup

### 1. Install runtime dependencies

```bash
pip install -r requirements.txt
```

### 2. Optional: install test dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Configure environment

Copy `.env.example` values into your environment as needed:

```bash
OPENAI_API_KEY=sk-your-openai-compatible-key
HF_TOKEN=hf_your_token_here
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
SEED=42
USE_LLM=false
```

## Local run instructions

### Deterministic inference run

```bash
python inference.py
```

### LLM-backed inference run

```bash
USE_LLM=true HF_TOKEN=hf_your_token_here python inference.py
```

### Run tests

```bash
python -m pytest tests -v
```

## Docker run instructions

Build image:

```bash
docker build -t ai-business-growth .
```

Run deterministic mode:

```bash
docker run --rm ai-business-growth
```

Run LLM mode:

```bash
docker run --rm \
  -e USE_LLM=true \
  -e HF_TOKEN=hf_your_token_here \
  -e API_BASE_URL=https://api.openai.com/v1 \
  -e MODEL_NAME=gpt-4o-mini \
  ai-business-growth
```

## Hugging Face Spaces deployment

Use a **Docker Space**.

1. Create a Space with SDK set to `Docker`.
2. Push this repository (root `Dockerfile` is used by Spaces).
3. Configure secrets:
   - `HF_TOKEN` (required only if `USE_LLM=true`)
4. Configure variables (optional):
   - `USE_LLM=false`
   - `API_BASE_URL=https://api.openai.com/v1`
   - `MODEL_NAME=gpt-4o-mini`
   - `SEED=42`
5. Confirm startup logs show `[START]` and completion logs show `[END]`.

## Error behavior

If initialization or runtime fails:

- `inference.py` emits a `[STEP]` payload with an `error` field
- `done` is set to `true`
- reward is emitted as `"0.00"`
- `[END]` is always printed

This prevents evaluator hangs and keeps output parseable.

## Reproducibility

Determinism controls:

- fixed default `SEED=42`
- deterministic heuristic fallback policy
- `temperature=0.0` for LLM action selection
- no wall-clock based randomness in environment transitions

Reproduce baseline output:

```bash
SEED=42 USE_LLM=false python inference.py
```

## Submission checklist

- [x] Root `inference.py` exists
- [x] `API_BASE_URL` default implemented
- [x] `MODEL_NAME` default implemented
- [x] `HF_TOKEN` validation implemented
- [x] OpenAI Python client is the only LLM SDK used in runtime path
- [x] Output contract `[START]` / `[STEP]` / `[END]` implemented
- [x] Lowercase JSON booleans guaranteed
- [x] Rewards formatted to 2 decimals
- [x] `[END]` always emitted, including error path
- [x] Root Dockerfile included for Hugging Face Spaces
