# ============================================================================
# Traffic Generator - Cisco Router Syslog Simulator
# Generates fake background traffic to make dashboards look "live"
# ============================================================================
FROM python:3.9-slim

# Install minimal dependencies
RUN pip install --no-cache-dir requests urllib3

# Create app directory
WORKDIR /app

# Copy simulation script
COPY simulate.py /app/simulate.py

# Run the traffic generator
CMD ["python", "-u", "/app/simulate.py"]
