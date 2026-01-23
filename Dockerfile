# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY app/mlapi.py .
COPY app/index.html .

# Copy models directory with all model files
COPY app/models/ ./models/

# Copy images directory
COPY app/img/ ./img/

# Verify files are copied correctly
RUN echo "=== Checking copied files ===" && \
    ls -la && \
    echo "=== Models directory ===" && \
    ls -la models/ && \
    echo "=== Images directory ===" && \
    ls -la img/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "mlapi:app", "--host", "0.0.0.0", "--port", "8000"]
