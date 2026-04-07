# AI Business Growth OpenEnv — Hackathon Edition

**Production-ready OpenEnv-style reinforcement learning environment for small business decision-making. Deterministic, low-resource, fully compliant with Meta PyTorch OpenEnv Hackathon requirements.**

---

## Quick Start (TL;DR)

```bash
# 1. Clone and install
git clone <your-repo-url>
cd opencv_pro-main
pip install -r requirements.txt

# 2. Run deterministic inference (no API key required)
python inference.py

# 3. Expected output
# [START]
# [STEP]
# {"task_id":1,"step":1,"action":"add_hashtags",...}
# [STEP]
# ...
# [END]
```

---

## What Is This?

This environment simulates real small business decision-making across three difficulty levels:

| Task | Description | Difficulty | Steps | Goal |
|------|-------------|-----------|-------|------|
| **Task 1** | Social Media Growth | Easy | 10 | 1000 followers + 5% engagement |
| **Task 2** | Review Management | Medium | 12 | 4.0 rating + 0.7 sentiment |
| **Task 3** | Revenue Optimization | Hard | 15 | ₹120K revenue + 0.7 satisfaction |

Each environment follows the **OpenEnv standard loop**:

```python
obs = env.reset()                 # Get initial observation
for step in range(max_steps):
    action = agent.choose(obs)    # Your agent decides
    result = env.step(action)     # Environment transitions
    obs = result.observation      # Updated state
    if result.done: break
```

---

## Interface

### Action Space

Actions are JSON objects specifying one decision per step:

```json
{"action_type":"generate_post","parameters":{"quality":4}}
{"action_type":"reply_review","parameters":{"tone":"professional"}}
{"action_type":"run_campaign","parameters":{"type":"social","budget":4000}}
{"action_type":"launch_bundle","parameters":{"items":["coffee","snack"],"bundle_price":210.0}}
{"action_type":"no_op","parameters":{}}
```

### Observation Space

Every observation exposes:

```python
{
    "task_id": 1,
    "step": 3,
    "metrics": {
        "followers": 720,
        "engagement_rate": 0.038,
        "avg_rating": 0.0,
        "monthly_revenue": 0.0,
        ...
    },
    "recent_actions": ["add_hashtags", "schedule_post"],
    "trend": "growing",
    "valid_actions": ["generate_post", "add_hashtags", "schedule_post", ...],
    "task_description": "...",
    "hint": null,
}
```

### Reward Design

Continuous shaped rewards with components:

- **Progress**: +0.0 to +1.0 based on metric improvement
- **No-op penalty**: -0.1 when choosing `no_op`
- **Spam penalty**: -0.2 when repeating actions excessively
- **Destructive penalty**: -0.5 when undoing progress
- **Goal bonus**: +2.0 when reaching task goal
- **Terminal bonus**: +1.0 for completing episode successfully

---

## Setup

### Prerequisites

- Python 3.9+
- pip or conda
- 2 vCPU / 8 GB RAM minimum (tested on HF Spaces)
- (Optional) OpenAI API key for LLM-backed agent

### Installation

**Option 1: Pip (Recommended)**

```bash
pip install -r requirements.txt
```

**Option 2: Conda**

```bash
conda create -n openenv python=3.11
conda activate openenv
pip install -r requirements.txt
```

**Option 3: Docker**

```bash
docker build -t openenv-hackathon:latest -f deployment/Dockerfile .
docker run -it \
  -e SEED=42 \
  -e USE_LLM=false \
  openenv-hackathon:latest
```

### Configuration

**File: `.env`** (copy from `.env.example` and fill in your keys)

```bash
# Required for LLM mode only (set USE_LLM=true to enable)
OPENAI_API_KEY=sk-your-key-here
HF_TOKEN=hf_your_token_here

# Hackathon defaults (do not change)
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini

# Runtime configuration
USE_LLM=false        # Use LLM agent if true, heuristic if false
SEED=42              # Deterministic seed
MODEL_TEMPERATURE=0.0
```

---

## Usage

### 1. Deterministic Inference Run (No API Key)

Runs 3 tasks with a heuristic policy. Deterministic, fast, suitable for evaluation.

```bash
python inference.py
```

**Output:**
```
[START]
[STEP]
{"task_id":1,"step":1,"action":"add_hashtags","reward":"0.05","done":false,"goal_reached":false}
[STEP]
...
[END]
```

### 2. OpenAI LLM-Backed Run

Uses OpenAI GPT-4o-mini to generate intelligent actions.

```bash
USE_LLM=true OPENAI_API_KEY=sk-your-key python inference.py
```

### 3. Local Interactive CLI

Explore all capabilities via interactive menu.

```bash
python main.py
```

### 4. Run Tests

```bash
pytest tests -v
```

Contract validation:
```bash
python tests/test_inference_contract.py
```

### 5. Docker Deployment

**Build:**
```bash
docker build -t openenv-hackathon:latest -f deployment/Dockerfile .
```

**Run:**
```bash
docker run -it \
  -e SEED=42 \
  -e USE_LLM=false \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  openenv-hackathon:latest
```

**Check Container Resource Usage:**
```bash
docker stats openenv-inference
```

---

## Hugging Face Spaces Deployment

### Step 1: Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Create new space → **Docker** runtime
3. Set visibility: **Public**

### Step 2: Upload Repository

```bash
git init
git add .
git commit -m "OpenEnv hackathon submission"
git remote add origin https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE_NAME
git push -u origin main
```

### Step 3: Configure Secrets

1. Navigate to: **Settings → Secrets**
2. Add:
   - `OPENAI_API_KEY`: Your OpenAI key (optional, for LLM mode)
   - `HF_TOKEN`: Your HF token (optional)

### Step 4: Monitor Build & Logs

- HF Spaces automatically builds from `Dockerfile`
- Logs available in **Settings → Logs**
- Container runs with: `SEED=42`, `USE_LLM=false` by default

**Expected Startup Time:** < 5 minutes on HF Spaces  
**Expected Memory Usage:** < 500 MB  
**Expected CPU Usage:** < 1 vCPU

---

## Hackathon Compliance Checklist

✅ **Output Format**
- `[START]` emitted at beginning
- `[STEP]` + JSON payload repeated each step
- `[END]` emitted always, even on errors
- JSON booleans lowercase (`true`, `false`)
- Rewards formatted to 2 decimals

✅ **Environment Setup**
- `API_BASE_URL` default: `https://api.openai.com/v1`
- `MODEL_NAME` default: `gpt-4o-mini`
- `HF_TOKEN` validated when `USE_LLM=true`
- OpenAI Python client used exclusively

✅ **Resource Constraints**
- Tested on 2 vCPU / 8 GB RAM
- Docker image: < 800 MB
- Inference latency: < 100ms per step (heuristic), < 5s (LLM)

✅ **Determinism & Reproducibility**
- `SEED=42` ensures reproducible behavior
- No non-deterministic operations in core loop
- Heuristic baseline independent of external state

✅ **Documentation**
- README with setup, usage, deployment
- DEVELOPMENT.md for local development
- HACKATHON_CHECKLIST.md for submission validation

---

## Development Guide

See [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Local testing
- Adding custom tasks
- Extending action space
- Custom graders

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker troubleshooting
- Performance optimization
- HF Spaces best practices

---

## Troubleshooting

### `[END]` not emitted on error

**Issue:** Exception causes early exit without `[END]`.  
**Fix:** Already handled in inference.py; ensure `finally:` block runs.

```python
try:
    runner.run()
except Exception as exc:
    # ... emit error step
finally:
    print("[END]")
```

### `HF_TOKEN is required when USE_LLM=true`

**Issue:** Missing or empty HF_TOKEN environment variable.  
**Fix:** Set before running:

```bash
export HF_TOKEN=hf_your_token_here
USE_LLM=true python inference.py
```

### Docker image size too large

**Issue:** `docker images` shows > 1 GB.  
**Fix:** Ensure using slim base image and layer caching:

```bash
docker build --build-arg BUILDKIT_INLINE_CACHE=1 \
  --progress=plain -t openenv:latest -f deployment/Dockerfile .
```

### Determinism broken on HF Spaces

**Issue:** Different results each run.  
**Fix:** Verify `SEED=42` set in environment; check that heuristic baseline doesn't use `random` calls.

---

## Project Structure

```
.
├── inference.py                # Canonical entrypoint
├── config/
│   └── openenv.yaml           # Environment configuration
├── env/
│   ├── business_env.py        # Core OpenEnv interface
│   ├── models/schemas.py      # Pydantic dataclasses
│   └── tasks/                 # Task implementations
├── agent/
│   ├── openai_client.py       # OpenAI client factory
│   ├── action_parser.py       # Action parsing utilities
│   └── prompts.py             # LLM system prompts
├── tests/
│   └── test_inference_contract.py  # Output format validation
└── scripts/
    └── validate_env.py        # Environment validation
```

---

## Citation

If you use this environment in research, please cite:

```bibtex
@misc{openenv-business-growth,
  title={AI Business Growth OpenEnv},
  author={Your Name},
  year={2025},
  publisher={GitHub},
  howpublished={\url{https://github.com/your-username/opencv_pro-main}}
}
```

---

## License

[MIT License](LICENSE) — See LICENSE file for details.

---

## Submission Status

- [x] Inference.py at repository root
- [x] OpenAI client usage (no SDK other than openai)
- [x] API_BASE_URL + MODEL_NAME defaults
- [x] HF_TOKEN validation
- [x] Output format: [START] / [STEP] / [END]
- [x] Rewards to 2 decimals
- [x] Lowercase JSON booleans
- [x] [END] emitted on exceptions
- [x] Deterministic heuristic baseline
- [x] Dockerfile for HF Spaces
- [x] Resource-optimized (< 8 GB, 2 vCPU)
- [x] Complete documentation
- [ ] **PENDING: Finalist review**

---

**Last Updated:** April 2025  
**Status:** Ready for Submission ✅
