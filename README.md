# 🔓 PwnageBox Public Portfolio Lab

**AI-Powered Offensive Security Simulation Platform**

A production-ready, Dockerized cyber attack simulation lab designed for portfolio demonstration. Features a beautiful web interface, real-time Splunk SIEM integration, and hardened security controls.

![Version](https://img.shields.io/badge/version-2.0-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 🎯 Overview

PwnageBox simulates a complete cyber attack chain against a vulnerable target, demonstrating:

- **Reconnaissance** - Nmap scanning and banner grabbing
- **Vulnerability Analysis** - CVE identification and matching
- **Exploitation** - Simulated Metasploit module execution
- **Post-Exploitation** - Root shell establishment

All activity is logged to Splunk Enterprise for real-time visualization.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        pwn_net (172.30.0.0/24)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │  Web UI     │    │   Splunk    │    │   Traffic Gen       │ │
│  │  :80        │    │   :8000     │    │   (Background)      │ │
│  │  Flask +    │    │   :8088 HEC │    │   Cisco Syslog      │ │
│  │  Auth/Rate  │    │             │    │                     │ │
│  │  172.30.0.50│    │ 172.30.0.10 │    │   172.30.0.40       │ │
│  └──────┬──────┘    └──────▲──────┘    └──────────┬──────────┘ │
│         │                  │                      │             │
│         │ Restart          │ HEC Logs             │ HEC Logs    │
│         ▼                  │                      │             │
│  ┌─────────────┐           │                      │             │
│  │  PwnBox     ├───────────┴──────────────────────┘             │
│  │  (Attacker) │                                                │
│  │  Nmap+Python│                                                │
│  │  172.30.0.30│                                                │
│  └──────┬──────┘                                                │
│         │                                                       │
│         │ Attack                                                │
│         ▼                                                       │
│  ┌─────────────┐                                                │
│  │ Victim-FTP  │                                                │
│  │ vsftpd 2.3.4│                                                │
│  │ CVE-2011-   │                                                │
│  │ 2523        │                                                │
│  │ 172.30.0.20 │                                                │
│  └─────────────┘                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- 4GB+ RAM recommended
- Ports 80, 8000, 8088 available

### Installation

```bash
# Clone the repository
git clone https://github.com/willynikes2/PwnageBox.git
cd PwnageBox/lab

# Configure environment
cp .env.example .env
# Edit .env and set your RECRUITER_PASSWORD

# Start the lab
chmod +x start.sh
./start.sh

# Or manually
docker-compose up -d --build
```

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Web UI | http://localhost:80 | Access Code (from .env) |
| Splunk | http://localhost:8000 | admin / PwnageBox2024! |

---

## 🔐 Security Features

### Authentication
- Attack trigger requires valid access code
- Password set via `RECRUITER_PASSWORD` environment variable

### Rate Limiting
- Global 45-second cooldown between attacks
- Prevents abuse and resource exhaustion

### Resource Limits
All containers have CPU/memory limits:

| Container | CPU | Memory |
|-----------|-----|--------|
| Splunk | 1.0 | 1024M |
| PwnBox | 0.5 | 512M |
| Web UI | 0.5 | 256M |
| Victim | 0.25 | 128M |
| Traffic Gen | 0.25 | 128M |

### Network Isolation
- Internal Docker network (pwn_net)
- Only ports 80, 8000, 8088 exposed externally

---

## 📊 Splunk Dashboard

The included dashboard provides:

- **Alert Status** - Real-time compromise indicator
- **Threat Map** - Geographic visualization of traffic sources
- **Kill Chain Timeline** - Attack progression events
- **Traffic Analysis** - Event volume over time
- **CVE Detections** - Identified vulnerabilities

### Importing the Dashboard

1. Log into Splunk at http://localhost:8000
2. Go to Settings → User Interface → Views
3. Create new dashboard from `splunk/dashboard.xml`

---

## 🎮 Usage

### Triggering an Attack

1. Open http://localhost:80
2. Click **"Initialize Attack Chain"**
3. Enter your access code (from .env)
4. Watch the kill chain progress in real-time
5. View detailed logs in Splunk

### Attack Stages

1. **INIT** - Attack chain initialization
2. **RECON** - Port scanning and banner grabbing
3. **VULN** - CVE identification (CVE-2011-2523)
4. **EXPLOIT** - Metasploit module simulation
5. **SUCCESS** - Root shell establishment

---

## 📁 Project Structure

```
pwnagebox-lab/
├── docker-compose.yml     # Service orchestration
├── .env.example           # Environment template
├── start.sh               # Startup script
├── README.md              # This file
│
├── pwnbox/
│   ├── Dockerfile         # Attack container
│   └── auto_pwn.py        # Attack logic
│
├── victim/
│   └── Dockerfile         # Vulnerable FTP server
│
├── traffic-gen/
│   ├── Dockerfile         # Traffic generator
│   └── simulate.py        # Cisco syslog simulator
│
├── web-ui/
│   ├── Dockerfile         # Web interface
│   ├── app.py             # Flask controller
│   ├── templates/
│   │   └── index.html     # Main interface
│   └── static/
│
└── splunk/
    └── dashboard.xml      # SOC dashboard
```

---

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SPLUNK_PASSWORD` | PwnageBox2024! | Splunk admin password |
| `SPLUNK_TOKEN` | pwnagebox-hec-token-2024 | HEC authentication token |
| `RECRUITER_PASSWORD` | YOURPASSWORD | Web UI access code |
| `RATE_LIMIT_SECONDS` | 45 | Cooldown between attacks |

---

## 🔧 Troubleshooting

### Splunk won't start
```bash
# Check logs
docker logs splunk

# Ensure port 8000 is available
lsof -i :8000
```

### Attack button disabled
- Wait for 45-second cooldown
- Check browser console for errors

### No logs in Splunk
```bash
# Verify HEC is working
curl -k https://localhost:8088/services/collector/health
```

---

## 👤 Author

**Shawn Daniel**  
Presient Labs  
[GitHub](https://github.com/willynikes2/PwnageBox)

---

## ⚠️ Disclaimer

This tool is for **authorized security testing and educational purposes only**. Do not use against systems you don't own or have explicit permission to test. The vulnerable components are intentionally insecure for demonstration purposes.

---

## 📄 License

MIT License - See LICENSE file for details.
