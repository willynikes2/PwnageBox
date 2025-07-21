# PwnageBox: Autonomous AI Cybersecurity Platform

## Overview
PwnageBox is a plug-and-pwn AI-powered cybersecurity device that autonomously scans, exploits, and reports on vulnerabilities in any target environment — digital or human.

## Features
- Multi-radio scanning and fingerprinting
- Exploit reasoning and zero-day discovery
- Goal-driven exploit executor
- Social engineering simulations with voice cloning

## Installation

### Prerequisites
- Python 3.9 or newer
- pip

### Install dependencies
```bash
pip install .
```

## Usage

### Run locally
```bash
uvicorn pwnagebox.app:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t pwnagebox .
docker run -d -p 8000:8000 pwnagebox
```

### API Endpoints
- `GET /` : Welcome message.
- `POST /scan` : Perform environment scan.
- `POST /research` : Analyze vulnerabilities.
- `POST /exploit` : Execute exploits.
- `POST /social_engineering` : Conduct social engineering attack.

## System Modules
- **Scammer:** Recon AI for environment scanning and fingerprinting.
- **Researcher:** Exploit reasoning AI.
- **Pwner:** Exploit execution engine.
- **VoicePwner:** Social engineering module with voice synthesis.

## Reporting
- Generates encrypted vulnerability reports.
- Supports Markdown, HTML, and PDF formats.
