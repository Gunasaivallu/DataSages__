FROM python:3.11-slim

WORKDIR /app

# CRITICAL FIX 1: Add /app/src to PYTHONPATH so Python can find your modules (agents, executor, etc.)
ENV PYTHONPATH=/app:/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all folders (frontend, src, etc.) into /app
COPY . .

# Hugging Face Spaces default port
EXPOSE 7860

# Launch both services
# CRITICAL FIX 2: Changed "backend.main:app" to "src.main:app"
# CRITICAL FIX 3: Added flags to disable CORS/XSRF protection for Streamlit
CMD sh -c "\
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/app.py --server.port=7860 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false \
"