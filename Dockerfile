# ------------------------------------
# Simple Single Container Setup
# ------------------------------------
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose Hugging Face Space port
EXPOSE 7860

# Start both backend and frontend
# Backend on port 8000, Frontend on port 7860
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & \
    sleep 3 && \
    streamlit run app.py --server.port=7860 --server.address=0.0.0.0