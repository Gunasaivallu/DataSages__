# ------------------------------------
# Single Container: Frontend + Backend
# ------------------------------------
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Install OS deps
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /app/backend/agents /app/backend/executor /app/backend/schemas /app/frontend

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY main.py /app/backend/main.py
COPY dataset_analyzer.py /app/backend/agents/dataset_analyzer.py
COPY planner.py /app/backend/agents/planner.py
COPY explainer.py /app/backend/agents/explainer.py
COPY executor.py /app/backend/executor/executor.py
COPY plan_validator.py /app/backend/schemas/plan_validator.py
COPY config.py /app/backend/config.py

# Copy frontend files
COPY app.py /app/frontend/app.py

# Create empty __init__.py files for Python modules
RUN touch /app/backend/__init__.py \
    /app/backend/agents/__init__.py \
    /app/backend/executor/__init__.py \
    /app/backend/schemas/__init__.py

# Expose port (Hugging Face expects 7860)
EXPOSE 7860

# Start backend + frontend
CMD sh -c "\
cd /app/backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 & \
cd /app/frontend && streamlit run app.py --server.port=7860 --server.address=0.0.0.0 \
"