FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

EXPOSE 8000

# Use Railway's PORT env var with fallback for local
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
