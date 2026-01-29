FROM python:3.11-slim

WORKDIR /app

# Fixes the ModuleNotFoundError by adding the current dir to Python's search path
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all folders (backend, agents, etc.) into /app
COPY . .

# Hugging Face Spaces default port
EXPOSE 7860

# Launch both services
CMD sh -c "\
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/app.py --server.port=7860 --server.address=0.0.0.0 \
"