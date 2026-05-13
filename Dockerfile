# ── Stage 1: Base ──────────────────────────────────────────
FROM python:3.11-slim AS base

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Test ──────────────────────────────────────────
FROM base AS test
COPY . .
RUN pytest tests/ -v --tb=short

# ── Stage 3: Production ────────────────────────────────────
FROM base AS production
COPY app/ ./app/
EXPOSE 5000
CMD ["python", "app/app.py"]
