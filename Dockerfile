FROM python:3.11-slim

WORKDIR /app

# Core environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
# This fixes the ModuleNotFoundError
ENV PYTHONPATH=/app 

# Install dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Hugging Face Spaces uses 7860 by default
EXPOSE 7860

# Start Backend on 8000 and Frontend on 7860
CMD sh -c "\
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/app.py --server.port=7860 --server.address=0.0.0.0 \
"