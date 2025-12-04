# ============================================================================
# Web UI - Flask Controller with Docker Management
# Provides public portfolio interface with authenticated attack trigger
# ============================================================================
FROM python:3.9-slim

# Install Docker CLI for container management
RUN apt-get update && \
    apt-get install -y \
        curl \
        ca-certificates \
        gnupg \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && chmod a+r /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    docker \
    requests \
    gunicorn

# Create app directory
WORKDIR /app

# Copy application files
COPY app.py /app/app.py
COPY templates/ /app/templates/
COPY static/ /app/static/

EXPOSE 5000

# Run with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
