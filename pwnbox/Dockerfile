# ============================================================================
# PwnBox - Attack Simulation Engine
# Contains: Nmap, Python attack logic, Splunk HEC integration
# ============================================================================
FROM python:3.9-slim

# Install Nmap and network utilities
RUN apt-get update && apt-get install -y \
    nmap \
    netcat-openbsd \
    curl \
    iputils-ping \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    requests \
    python-nmap \
    urllib3

# Create app directory
WORKDIR /app

# Copy attack script
COPY auto_pwn.py /app/auto_pwn.py

# Make script executable
RUN chmod +x /app/auto_pwn.py

# Run the attack simulation on container start
CMD ["python", "-u", "/app/auto_pwn.py"]
