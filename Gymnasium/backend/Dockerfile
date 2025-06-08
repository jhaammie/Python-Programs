# === Build Stage ===
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (optional but good if you have wheels, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environment in build stage
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy only requirements first to cache layers
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# === Final Stage ===
FROM python:3.11-slim AS final

WORKDIR /app

# Copy virtual environment from build stage
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy app source
COPY . .

# Expose FastAPI port
EXPOSE 5006

# Run with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5006"]
