#!/bin/bash
# ============================================================================
# PwnageBox Lab Startup Script
# ============================================================================

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   ██████╗ ██╗    ██╗███╗   ██╗ █████╗  ██████╗ ███████╗      ║"
echo "║   ██╔══██╗██║    ██║████╗  ██║██╔══██╗██╔════╝ ██╔════╝      ║"
echo "║   ██████╔╝██║ █╗ ██║██╔██╗ ██║███████║██║  ███╗█████╗        ║"
echo "║   ██╔═══╝ ██║███╗██║██║╚██╗██║██╔══██║██║   ██║██╔══╝        ║"
echo "║   ██║     ╚███╔███╔╝██║ ╚████║██║  ██║╚██████╔╝███████╗      ║"
echo "║   ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ║"
echo "║                        BOX v2.0                               ║"
echo "║                    Lab Startup Script                         ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "[!] No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "[!] IMPORTANT: Edit .env to set your RECRUITER_PASSWORD!"
    echo ""
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "[✗] Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "[✗] Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "[*] Starting PwnageBox Lab..."
echo ""

# Use docker compose (v2) or docker-compose (v1)
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Build and start
$COMPOSE_CMD down --remove-orphans 2>/dev/null || true
$COMPOSE_CMD build --no-cache
$COMPOSE_CMD up -d

echo ""
echo "============================================================"
echo "PwnageBox Lab is starting up!"
echo "============================================================"
echo ""
echo "Services:"
echo "  • Web UI:    http://localhost:80"
echo "  • Splunk:    http://localhost:8000"
echo ""
echo "Splunk Credentials:"
echo "  • Username:  admin"
echo "  • Password:  PwnageBox2024! (or check SPLUNK_PASSWORD in .env)"
echo ""
echo "Waiting for services to be ready..."
echo ""

# Wait for Splunk
echo -n "[*] Waiting for Splunk (this may take 2-3 minutes)"
for i in {1..60}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|302\|303"; then
        echo ""
        echo "[✓] Splunk is ready!"
        break
    fi
    echo -n "."
    sleep 5
done

# Check web UI
echo -n "[*] Waiting for Web UI"
for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:80 | grep -q "200"; then
        echo ""
        echo "[✓] Web UI is ready!"
        break
    fi
    echo -n "."
    sleep 2
done

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "Next Steps:"
echo "1. Open http://localhost:80 in your browser"
echo "2. Click 'Initialize Attack Chain' and enter your access code"
echo "3. Watch the attack unfold in real-time"
echo "4. View detailed logs in Splunk at http://localhost:8000"
echo ""
echo "To stop the lab:"
echo "  $COMPOSE_CMD down"
echo ""
