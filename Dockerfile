# ── Stage 1: Build the React frontend ────────────────────────────────────────
FROM node:20-slim AS frontend-builder

WORKDIR /build/dashboard-ui

# Install dependencies (cache layer)
COPY dashboard-ui/package.json dashboard-ui/package-lock.json ./
RUN npm ci --prefer-offline

# Copy source and build
COPY dashboard-ui/ ./
RUN npm run build

# ── Stage 2: Python runtime + FastAPI server ──────────────────────────────────
FROM python:3.11-slim

# Set environment for reproducibility and efficiency
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    PORT=7860 \
    SEED=42 \
    USE_LLM=false \
    API_BASE_URL=https://api.openai.com/v1 \
    MODEL_NAME=gpt-4o-mini

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

# Copy application source
COPY agent ./agent
COPY env ./env
COPY config ./config
COPY inference.py .
COPY app.py .

# Copy the built React frontend from the first stage
COPY --from=frontend-builder /build/dashboard-ui/dist ./dashboard-ui/dist

# Create a non-root user (required by Hugging Face Spaces)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

# Start the FastAPI server
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]