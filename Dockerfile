FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The source PDF must be mounted or placed in data/
VOLUME ["/app/data"]

# Default: run the full pipeline
CMD ["python", "src/setup_multiplex_db.py"]
