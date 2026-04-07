# AegisTrader Dockerfile
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create app user
RUN groupadd -r aegistrader && useradd -r -g aegistrader aegistrader

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=aegistrader:aegistrader . .

# Create necessary directories
RUN mkdir -p data logs models screenshots && \
    chown -R aegistrader:aegistrader /app

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    HEADLESS_BROWSER=true \
    DISPLAY=:99

# Create startup script
RUN echo '#!/bin/bash\n\
# Start virtual display for headless browser\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
\n\
# Wait for display to be ready\n\
sleep 2\n\
\n\
# Start AegisTrader\n\
exec python main.py\n\
' > /app/start.sh && \
    chmod +x /app/start.sh && \
    chown aegistrader:aegistrader /app/start.sh

# Switch to app user
USER aegistrader

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Expose port for monitoring (optional)
EXPOSE 8080

# Start application
CMD ["/app/start.sh"]
