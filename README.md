# PwnageBox

**PwnageBox** is an AI-powered offensive cybersecurity platform designed for network reconnaissance, vulnerability research, and automated exploitation. It combines multi-radio scanning (WiFi, Bluetooth, Zigbee, etc.) with agentic AI modules that simulate the behavior of expert red-teamers — including reconnaissance, fingerprinting, exploit matching, and real-world pwnage execution via tools like Metasploit.

Built for white hat and black hat simulation environments, PwnageBox provides a fully modular FastAPI backend with support for SQLite, Docker, and real-time AI decision-making.

---

## 🔥 Core Capabilities

- 🧠 **Scammer AI** – Performs active/passive radio-based scanning, identifies and fingerprints nearby devices.
- 🕵️ **Researcher AI** – Maps detected devices to known vulnerabilities (CVEs, exploit DBs, and zero-day heuristics).
- 💣 **Pwner AI** – Executes exploitation workflows, including direct integration with Metasploit.
- 🗣️ **VoicePwner AI** – Experimental module for voice cloning and social engineering simulation.
- 📡 Multi-radio support – Designed to interface with WiFi, Bluetooth, Zigbee, and SDR hardware.
- 📦 FastAPI-based backend with clean modular endpoints.
- 🐳 Dockerized deployment for edge devices or cloud simulation.
- 🧠 Powered by Codex + Context7 for continuous self-updating logic.
- 📄 Integrated with SQLite for audit trails and result persistence.

---

## 🧰 Tech Stack

- Python 3.12+
- FastAPI
- SQLite
- Docker
- OpenAI (Codex + GPT)
- Context7 for MCP/project context
- Metasploit Framework (optional, for exploitation module)

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/docs/#installation)
- Docker (for containerized deployment)
- Metasploit Framework (optional, for Pwner AI)

---

### 📦 Local Installation

```bash
poetry install
