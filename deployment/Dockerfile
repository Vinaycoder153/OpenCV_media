FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# OPENAI_API_KEY can be passed at run-time:
#   docker run -e OPENAI_API_KEY=sk-... ai-business-growth
CMD ["python", "agent/baseline_agent.py"]
