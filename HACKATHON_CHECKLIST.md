# Hackathon Submission Checklist

**Use this checklist before final submission to ensure 100% compliance with Meta PyTorch OpenEnv Hackathon requirements.**

---

## Critical Requirements (MUST PASS)

### Output Format

- [ ] `[START]` is printed as the very first line
- [ ] Every action emits `[STEP]` on its own line
- [ ] Every `[STEP]` is followed by exactly one line of JSON
- [ ] `[END]` is printed as the very last line
- [ ] `[END]` is printed **even if an exception occurs**
- [ ] No extra whitespace or text between markers

**Test:**
```bash
python inference.py | head -3
# Output should be:
# [START]
# [STEP]
# {"..."}
```

---

### JSON Output Format

- [ ] All JSON output is valid JSON (parseable)
- [ ] Booleans are lowercase: `true`, `false` (not `True`, `False`)
- [ ] Rewards are formatted as strings with exactly 2 decimals
  - ✅ `"reward": "0.50"`
  - ✅ `"reward": "0.00"`
  - ❌ `"reward": 0.5`
  - ❌ `"reward": "0.5"` (not 2 decimals)
- [ ] All required fields present in each step
- [ ] No NaN, Infinity, or null values in numeric fields

**Test:**
```bash
python inference.py 2>&1 | grep '"\w*":\s*true'
# Should find lowercase: true/false (not True/False)
```

---

### API Configuration

- [ ] `API_BASE_URL` defaults to `https://api.openai.com/v1`
- [ ] `MODEL_NAME` defaults to `gpt-4o-mini`
- [ ] Code uses only the OpenAI Python SDK (`from openai import OpenAI`)
- [ ] No other LLM SDK imports (no `google-generativeai`, `anthropic`, etc.)
- [ ] HF_TOKEN is validated with clear error message when `USE_LLM=true`

**Test:**
```bash
grep -r "from openai import" .
grep -r "from google" .  # Should find NOTHING
grep -r "import google" .  # Should find NOTHING
```

---

### Token & Authentication

- [ ] `.env.example` contains **NO real API keys** (only placeholders)
- [ ] `.gitignore` includes `.env` and secrets/
- [ ] Real `.env` file is never committed
- [ ] `HF_TOKEN` environment variable is validated on startup

**Test:**
```bash
# Review .env.example
cat .env.example | grep -E "sk-|hf_"
# Should show PLACEHOLDER values only, not real keys

# Check git status
git status | grep ".env"
# Should NOT show .env (only .env.example)
```

---

### Determinism & Reproducibility

- [ ] `SEED=42` by default
- [ ] Running with same SEED produces identical action sequences
- [ ] No time-based randomness (no `time.time()`, no `random.random()`)
- [ ] Heuristic baseline uses no external state
- [ ] Temperature set to 0.0 for deterministic LLM behavior

**Test:**
```bash
# Run twice and compare
python inference.py > run1.txt
python inference.py > run2.txt
diff run1.txt run2.txt
# Should show NO differences
```

---

### Hackathon Entrypoint

- [ ] `inference.py` exists at repository root (not in subdirectory)
- [ ] `inference.py` is directly executable: `python inference.py`
- [ ] Can run without command-line arguments: `python inference.py` (uses env vars only)
- [ ] Completes all 3 tasks in < 2 minutes (heuristic mode)

**Test:**
```bash
cd /repo/root
python inference.py | tail -5
# Should see [END] within 2 minutes
```

---

## High-Priority Compliance (SHOULD PASS)

### Docker Deployment

- [ ] `Dockerfile` exists at repository root or in `deployment/` directory
- [ ] Docker image builds successfully: `docker build -t openenv:latest -f deployment/Dockerfile .`
- [ ] Docker image runs successfully: `docker run openenv:latest`
- [ ] Docker image size < 1 GB: `docker images | grep openenv`
- [ ] Container completes in < 3 minutes

**Test:**
```bash
docker build -t openenv:test -f deployment/Dockerfile . && \
docker run -e SEED=42 -e USE_LLM=false openenv:test | tail -3
```

---

### Resource Constraints (HF Spaces)

- [ ] Runs on 2 vCPU / 8 GB RAM (tested locally)
- [ ] Memory usage < 500 MB
- [ ] CPU usage stays < 1 vCPU (heuristic) or < 2 vCPU (LLM)
- [ ] No memory leaks over multiple runs

**Test:**
```bash
# Monitor resource usage
docker run --memory=500m --cpus=2 openenv:latest

# Or check local process
python -c "
import psutil, os
p = psutil.Process(os.getpid())
print(f'Memory: {p.memory_info().rss/1024/1024:.0f} MB')
print(f'CPU: {p.cpu_num()} core(s)')
"
```

---

### Documentation

- [ ] `README.md` exists and includes:
  - [ ] What the environment does
  - [ ] Task descriptions and goals
  - [ ] Action space explanation
  - [ ] Observation space explanation
  - [ ] Setup instructions
  - [ ] Usage examples
  - [ ] Docker deployment steps
  - [ ] HF Spaces deployment steps
  - [ ] Troubleshooting section
  
- [ ] `DEVELOPMENT.md` exists and includes:
  - [ ] Local setup instructions
  - [ ] How to run tests
  - [ ] How to add new tasks
  
- [ ] `DEPLOYMENT.md` exists and includes:
  - [ ] Docker build/run instructions
  - [ ] HF Spaces step-by-step guide
  - [ ] Troubleshooting for deployment
  
- [ ] `HACKATHON_CHECKLIST.md` (this file) is present
- [ ] License file exists (`LICENSE`, typically MIT)

**Test:**
```bash
ls -la | grep -E "README|DEVELOPMENT|DEPLOYMENT|HACKATHON|LICENSE"
# Should find all files
```

---

### Code Quality

- [ ] No hardcoded API keys or secrets anywhere
- [ ] All public functions have docstrings
- [ ] Type hints present on main functions
- [ ] Comments explain non-obvious logic
- [ ] Code follows PEP 8 style guide
- [ ] Tests pass: `pytest tests -v`

**Test:**
```bash
pytest tests -v

python tests/test_inference_contract.py
```

---

## Pre-Submission Verification (FINAL)

Run this complete verification before uploading:

### 1. Local Test (No Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Validate environment
python scripts/validate_env.py

# Run inference
time python inference.py > /tmp/output.txt

# Check output
head -3 /tmp/output.txt  # Should see [START], [STEP], JSON
tail -3 /tmp/output.txt  # Should see [...], [STEP], [END]

# Contract tests
python tests/test_inference_contract.py
```

### 2. Docker Test

```bash
# Build image
docker build -t openenv:test -f deployment/Dockerfile .

# Check size
docker images | grep openenv

# Run inference
docker run -e SEED=42 -e USE_LLM=false openenv:test 2>&1 | tee /tmp/docker-output.txt

# Verify output
grep "\[START\]" /tmp/docker-output.txt  # Should find 1 match
grep "\[END\]" /tmp/docker-output.txt    # Should find 1 match
```

### 3. Git Verification

```bash
# Check no secrets committed
git log -p | grep -E "sk-|hf_" && echo "FAIL" || echo "PASS"

# Check git status clean
git status | grep "nothing to commit"

# Verify .env not in repo
git ls-files | grep -E "^\\.env$" && echo "FAIL" || echo "PASS"
```

### 4. Repository Structure

```bash
# Verify critical files exist
[ -f inference.py ] && echo "✅ inference.py" || echo "❌ inference.py"
[ -f README.md ] && echo "✅ README.md" || echo "❌ README.md"
[ -f DEVELOPMENT.md ] && echo "✅ DEVELOPMENT.md" || echo "❌ DEVELOPMENT.md"
[ -f DEPLOYMENT.md ] && echo "✅ DEPLOYMENT.md" || echo "❌ DEPLOYMENT.md"
[ -f deployment/Dockerfile ] || [ -f Dockerfile ] && echo "✅ Dockerfile" || echo "❌ Dockerfile"
[ -f requirements.txt ] && echo "✅ requirements.txt" || echo "❌ requirements.txt"
[ -f LICENSE ] && echo "✅ LICENSE" || echo "❌ LICENSE"
```

---

## Submission Readiness Matrix

| Category | Status | Evidence |
|----------|--------|----------|
| **Critical** | | |
| Output Format [START/END] | [ ] | `python inference.py` output |
| JSON Compliance | [ ] | `python tests/test_inference_contract.py` |
| API Defaults | [ ] | grep `API_BASE_URL`, `MODEL_NAME` |
| Determinism | [ ] | diff of two runs |
| Entrypoint | [ ] | `python inference.py` works |
| | | |
| **High-Priority** | | |
| Docker Build | [ ] | `docker build` succeeds |
| Docker Run | [ ] | `docker run` produces output |
| Documentation | [ ] | All .md files exist |
| No Secrets | [ ] | `.env.example` has placeholders |
| Tests Pass | [ ] | `pytest tests -v` exit 0 |
| | | |
| **Final Check** | | |
| Repository Clean | [ ] | `git status` shows nothing |
| HF Spaces Ready | [ ] | Can push and build |
| Submission Ready | [ ] | All above ✅ |

---

## Final Submission Steps

When all checkboxes are ✅:

1. **Commit Everything**
   ```bash
   git add .
   git commit -m "Hackathon submission: production-ready OpenEnv"
   git push origin main
   ```

2. **Create HF Space** (if not already done)
   - Go to: https://huggingface.co/spaces
   - Create new space (Docker SDK)
   - Configure secrets (OPENAI_API_KEY, HF_TOKEN optional)

3. **Push to HF Spaces**
   ```bash
   git remote add huggingface https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE_NAME
   git push huggingface main
   ```

4. **Verify HF Spaces Build**
   - Check **Settings → Logs**
   - Confirm `[START]` and `[END]` in logs
   - Verify < 15 minute build time

5. **Submit to Hackathon**
   - Note down GitHub repo URL
   - Note down HF Spaces URL
   - Submit both to hackathon portal
   - Include this checklist in submission notes

---

## Common Issues & Solutions

### `[END]` Missing

**Problem:** Output stops without `[END]`  
**Solution:** Check `finally:` block in inference.py runs on all paths

### JSON Parsing Fails

**Problem:** Evaluator can't parse JSON output  
**Solution:** Ensure rewards are strings: `"0.50"` not `0.5` or `"0.5"`

### Determinism Broken

**Problem:** Different results on second run  
**Solution:** Verify `SEED=42` environment variable and no randomness in heuristic

### Docker Image Too Large

**Problem:** Image > 1 GB  
**Solution:** Use `python:3.11-slim`, remove test deps, use `RUN --mount=type=cache`

### HF Spaces Timeout

**Problem:** Build takes > 15 minutes  
**Solution:** Reduce image size, check for slow pip installs

---

## Ready to Submit? Last Checklist

- [ ] All critical requirements ✅
- [ ] All high-priority requirements ✅
- [ ] All documentation complete ✅
- [ ] Tests passing ✅
- [ ] Docker working ✅
- [ ] HF Space built successfully ✅
- [ ] Repository clean (only .env untracked) ✅
- [ ] This checklist completely filled out ✅

---

## 🎉 Submission Ready!

**All checkboxes green?** You're ready to submit!

**Questions?** Check README.md, DEVELOPMENT.md, or DEPLOYMENT.md

**Last-minute changes?** Test locally, Docker, then push to HF Spaces

---

**Final Status:** ⏳ Ready for Review  
**Last Updated:** April 2025  
**Submitted:** ___/__/___
