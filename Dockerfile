FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/virtual_influencer_engine

# Set python path to include the current directory
ENV PYTHONPATH=/app

# Expose API port
EXPOSE 8000

# Run command
CMD ["uvicorn", "virtual_influencer_engine.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
