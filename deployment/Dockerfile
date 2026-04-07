FROM python:3.11-slim

# Set environment for reproducibility and efficiency
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy only requirements (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

# Copy minimal project structure (exclude unnecessary files)
COPY config ./config
COPY env ./env
COPY agent ./agent
COPY inference.py .

# Health check (optional but recommended for HF Spaces)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Entrypoint: canonical inference script
ENV SEED=42
ENV USE_LLM=false
ENV API_BASE_URL=https://api.openai.com/v1
ENV MODEL_NAME=gpt-4o-mini

ENTRYPOINT ["python", "inference.py"]
