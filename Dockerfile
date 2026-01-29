# ------------------------------------
# Single Container: Frontend + Backend
# ------------------------------------
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit
CMD sh -c "\
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 \
"
