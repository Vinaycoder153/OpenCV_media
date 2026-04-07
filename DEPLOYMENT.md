# Deployment Guide

Production deployment strategies for Docker, Hugging Face Spaces, and troubleshooting guides.

---

## Docker Build & Run

### Build Image

```bash
# Standard build
docker build -t openenv-hackathon:latest -f deployment/Dockerfile .

# Optimized build with caching
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --progress=plain \
  -t openenv-hackathon:latest \
  -f deployment/Dockerfile .
```

### Run Locally

**Deterministic (no API key needed):**

```bash
docker run -it \
  -e SEED=42 \
  -e USE_LLM=false \
  openenv-hackathon:latest
```

**With LLM (requires OpenAI key):**

```bash
docker run -it \
  -e SEED=42 \
  -e USE_LLM=true \
  -e OPENAI_API_KEY=sk-your-key \
  -e API_BASE_URL=https://api.openai.com/v1 \
  -e MODEL_NAME=gpt-4o-mini \
  openenv-hackathon:latest
```

### Check Image Size

```bash
docker images | grep openenv-hackathon
```

**Expected:** < 800 MB

---

## Docker Compose (Development)

**File: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  inference:
    build:
      context: .
      dockerfile: deployment/Dockerfile
    image: openenv-hackathon:latest
    container_name: openenv-inference
    environment:
      SEED: "42"
      USE_LLM: "false"
      API_BASE_URL: "https://api.openai.com/v1"
      MODEL_NAME: "gpt-4o-mini"
      # OPENAI_API_KEY: "${OPENAI_API_KEY:-}"    # Optional
    ports:
      - "8000:8000"  # If adding web interface
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 8G
        reservations:
          cpus: '1'
          memory: 4G
```

**Run:**

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Hugging Face Spaces

### Prerequisites

- GitHub account (optional, for syncing)
- Hugging Face account: https://huggingface.co
- Space creation permission

### Step 1: Create a New Space

1. Navigate to: https://huggingface.co/spaces
2. Click: **Create new Space**
3. Configure:
   - **Name**: `openenv-business-growth` (choose your name)
   - **License**: MIT (or your choice)
   - **Space SDK**: Docker
   - **Visibility**: Public
4. Click: **Create Space**

### Step 2: Push Repository

```bash
# Clone HF Space repo
git clone https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Add files from your project
# (Copy all files except .git directory)

# Commit and push
git add .
git commit -m "Initial commit: OpenEnv hackathon submission"
git push
```

**Alternative: Direct Git Push**

```bash
git remote add huggingface https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE_NAME
git push -u huggingface main
```

### Step 3: Configure Secrets & Variables

1. Go to: **Settings → Secrets & Variables**
2. Add **Secrets** (hidden from logs):
   - `OPENAI_API_KEY` (if using LLM mode)
   - `HF_TOKEN` (if needed)
3. Add **Variables** (visible):
   - `SEED=42`
   - `USE_LLM=false`
   - `API_BASE_URL=https://api.openai.com/v1`
   - `MODEL_NAME=gpt-4o-mini`

### Step 4: Monitor Build

1. Navigate to: **Settings → Logs**
2. Watch build process:
   - Docker build may take 3-5 minutes
   - Container starts automatically
   - Check for `[START]` and `[END]` markers

**Expected Log Output:**

```
[INFO] Building Docker image...
[SUCCESS] Docker image built successfully
[INFO] Starting container...
[START]
[STEP]
...
[END]
```

### Step 5: Test the Space

Visit: `https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE_NAME`

Check:
- ✅ Container is running
- ✅ Logs show `[START]` and `[END]`
- ✅ Output is properly formatted
- ✅ No errors or crashes

---

## Performance Optimization

### Memory Usage

Check current usage:

```bash
docker run -it \
  -e SEED=42 \
  -e USE_LLM=false \
  openenv-hackathon:latest \
  python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

**Expected:** < 500 MB

### CPU Usage

Monitor:

```bash
docker stats openenv-inference
```

**Expected:** < 1 vCPU for heuristic, < 2 vCPU for LLM

### Inference Latency

Measure:

```bash
import time
start = time.time()
runner.run()
elapsed = time.time() - start
print(f"Total time: {elapsed:.2f}s")
```

**Expected:** < 120 seconds total (heuristic), < 300 seconds (LLM)

### Optimize Image Size

**Current layers:**

```bash
docker history openenv-hackathon:latest
```

**Optimization checklist:**

- ✅ Using `python:3.11-slim` (not `python:3.11-bullseye`)
- ✅ Removed build tools after install
- ✅ No test dependencies in Docker
- ✅ Single-layer COPY for app code
- ✅ No `apt-get upgrade` (only specific packages)

---

## Troubleshooting

### Docker Build Fails

**Issue:** `ERROR: failed to solve: ...`

**Fix:**

```bash
# Clear cache and rebuild
docker builder prune
docker build --no-cache -t openenv-hackathon:latest -f deployment/Dockerfile .
```

### Container Exits Immediately

**Issue:** `docker run` starts but exits with no output

**Fix:**

```bash
# Check logs
docker run openenv-hackathon:latest 2>&1 | head -50

# Debug with bash
docker run -it openenv-hackathon:latest /bin/bash
```

### `[END]` Never Appears

**Issue:** Output stops after some `[STEP]` entries

**Fix:**

1. Check if process is alive:
   ```bash
   docker ps  # Should show running container
   ```
2. Add timeout and capture stderr:
   ```bash
   timeout 180 docker run openenv-hackathon:latest 2>&1
   ```
3. Veri fy exception handling in `inference.py`

### HF Spaces Build Timeout

**Issue:** Build takes > 15 minutes or times out

**Fix:**

1. Reduce Docker image size (see Optimization)
2. Check **Settings → Logs** for build errors
3. Try rebuilding: **Settings → Rebuild Space**

### Out of Memory on HF Spaces

**Issue:** Container crashes with OOM killer

**Fix:**

1. Reduce dependency overhead:
   ```bash
   # Check what's installed
   pip list
   # Remove unnecessary packages
   ```
2. Filter requirements.txt to only essential
3. Use `--no-cache-dir` in pip install (already in Dockerfile)

### API Key Not Recognized

**Issue:** `ValidationError: Invalid API key`

**Fix:**

1. Verify key format (OpenAI starts with `sk-`)
2. Check in HF Spaces: **Settings → Secrets** (not Variables)
3. Restart Space after updating secret

### Determinism Broken

**Issue:** Different outputs on each run

**Fix:**

1. Verify `SEED` is set to `42`:
   ```bash
   docker run -e SEED=DEBUG openenv-hackathon:latest python -c "import os; print(os.environ.get('SEED'))"
   ```
2. Ensure `USE_LLM=false` (RNG is deterministic)
3. Check no external randomness in code

---

## Production Checklist

Before final submission:

- [ ] Docker builds successfully
- [ ] Image size < 1 GB (`docker images`)
- [ ] Deterministic run produces same output twice
- [ ] Container runs on 2 vCPU / 8 GB RAM
- [ ] All environment variables documented
- [ ] `[START]` appears at beginning
- [ ] `[END]` appears at end (even on error)
- [ ] JSON output is valid (parseable)
- [ ] Rewards are 2 decimals
- [ ] No secrets in logs
- [ ] Heuristic baseline runs without API key
- [ ] LLM mode works with valid key
- [ ] All tests pass (`pytest tests -v`)
- [ ] HF Spaces build completes < 15 min
- [ ] Repository is clean (no uncommitted changes except `.env`)

---

## Performance Benchmarks

### Baseline System (2 vCPU, 8 GB RAM)

| Mode | Startup | Per-Step | Total 3 Tasks | Memory |
|------|---------|----------|---------------|--------|
| Heuristic | 2s | 5-10ms | 60-90s | 150 MB |
| LLM | 5s | 1-3s | 180-300s | 250 MB |

### HF Spaces Benchmarks

| Operation | Expected Time |
|-----------|-----------------|
| Git push to Space | 1-2 min |
| Docker build | 3-5 min |
| Container startup | 30-60 sec |
| Inference run (heuristic) | 60-120 sec |
| Total end-to-end | 5-10 min |

---

## Best Practices

### Security

- ✅ Never commit real API keys (use `.env.example` with placeholders)
- ✅ Use HF Spaces **Secrets**, not environment variables
- ✅ Rotate API keys regularly
- ✅ Don't log sensitive data

### Reliability

- ✅ Use `SEED=42` for reproducibility
- ✅ Always emit `[END]`, even on error
- ✅ Test locally before pushing to HF Spaces
- ✅ Use health checks (`HEALTHCHECK` in Dockerfile)

### Maintainability

- ✅ Document all environment variables
- ✅ Keep Docker image lean (slim base image)
- ✅ Use semantic versioning for tags
- ✅ Tag releases: `docker tag openenv:v1.0.0`

---

**Questions?** Check the README.md or open an issue!
