FROM python:3.11-slim

WORKDIR /app

# 1. FIX PATHS: Add /app/src to PYTHONPATH
ENV PYTHONPATH=/app:/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all folders
COPY . .

# 2. CREATE CONFIG FILE: This command writes the TOML settings to a file inside the container
RUN mkdir -p .streamlit && echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > .streamlit/config.toml

# Hugging Face Spaces default port
EXPOSE 7860

# 3. FIX COMMAND: Point to 'src.main:app' and use the config file we just made
CMD sh -c "\
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 & \
streamlit run frontend/app.py --server.port=7860 --server.address=0.0.0.0 \
"