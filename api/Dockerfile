# api/Dockerfile

# ===== BASE IMAGE =====
# Use official Python 3.12 slim image
# slim = smaller size, faster download
FROM python:3.12-slim

# ===== SET WORKING DIRECTORY =====
# All commands run from /app folder inside container
WORKDIR /app

# ===== INSTALL SYSTEM DEPENDENCIES =====
# These are needed for faiss and sentence-transformers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# ===== COPY REQUIREMENTS FIRST =====
# Copy requirements before code
# This way Docker caches libraries
# Only reinstalls if requirements.txt changes
COPY api/requirements.txt .

# ===== INSTALL PYTHON LIBRARIES =====
RUN pip install --no-cache-dir -r requirements.txt

# ===== COPY API CODE =====
# Copy entire api/ folder into container
COPY api/ .

# ===== COPY VECTOR STORE =====
# Copy FAISS index and metadata
# These are needed for the API to work
COPY vector_store/ ./vector_store/

# ===== COPY ENVIRONMENT FILE =====
# Only copy .env.example — real .env is set via Cloud Run
# COPY .env.example .env

# ===== CREATE OUTPUTS FOLDER =====
# Where generated documents are saved
RUN mkdir -p outputs

# ===== EXPOSE PORT =====
# Tell Docker this container uses port 8000
EXPOSE 8000

# ===== HEALTH CHECK =====
# Docker checks if container is healthy every 30 seconds
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=60s \
            --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ===== START COMMAND =====
# Run the FastAPI server when container starts
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1"]