# PwnageBox System Specification

**Version:** 2.0  
**Date:** 2025-07-21  
**Author:** Presient Systems

---

## 🧠 Overview

**PwnageBox** is a plug-and-play AI-powered cybersecurity appliance for offensive and defensive simulation, red teaming, and zero-day validation. It combines multi-radio scanning hardware with modular AI agents to autonomously identify, exploit, and verify vulnerabilities in networks and software systems. Built for both ethical hackers and enterprise red teams, PwnageBox is designed to function independently or in orchestrated clusters.

---

## 🚀 Features

### Core AI Modules
| Module        | Purpose                                                       |
|---------------|---------------------------------------------------------------|
| `scammer`     | Performs multi-radio reconnaissance (WiFi, BT, Zigbee, SDR)   |
| `researcher`  | Matches targets against CVEs, MCP databases, or theorizes 0-days |
| `pwner`       | Executes exploits using Metasploit or custom payloads         |
| `voicepwner`  | Uses voice cloning + scripts for social engineering           |

### Exploitation Integration
- Full Metasploit integration: Pwner AI can trigger exploits from Metasploit when high-confidence targets are found.
- Pre-configured module support for common exploits.
- Logs exploit success/failure in local database and Context7.

### Zero-Day Marketplace Pipeline
- 🔍 Hacker submits PoC anonymously (wallet-only)
- 🧪 AI deploys code in isolated Docker/LXD simulation
- 🤖 AI agent attempts to verify exploit effect
- ✅ If verified, payment is issued automatically via Lightning/ETH/USDC/etc
- 🧾 Log stored in secure audit trail for later inspection
- ❌ Invalid exploits are flagged and blacklisted

### Context7 Integration
- Used to store session history, logs, and regenerate agent plans
- Connected to Codex and Codex Agent

---

## 🧰 Integrated MCP Servers

| MCP Server       | Tool Used     | Functionality                                                  |
|------------------|---------------|----------------------------------------------------------------|
| `WireMCP`        | Wireshark     | Live capture, PCAP analysis, interface targeting               |
| `nmap-mcp-server`| Nmap          | Port scanning, OS fingerprinting, script engine                |
| `MCP-Snyk`       | Snyk API      | Vulnerability scan for repos, token-based org access           |
| `Semgrep MCP`    | Semgrep       | Static code analysis with rule customization                   |
| `HackerNews MCP` | Web crawler   | Search by keyword, scrape discussions, threat intelligence     |

These services are queried on demand by the AI modules to enrich recon and exploit research.

---

## 🛠️ Architecture

### Components
- `FastAPI` backend (REST + Web UI)
- `Docker` container for deployment
- `SQLite` for lightweight embedded storage
- `codex-agent` for local development / CI use
- `codex.yaml` for Context7 integration

### Directory Layout
```
pwnagebox/
├── app/
│   ├── ai_modules/
│   ├── routers/
│   ├── database.py
│   ├── main.py
├── modules/ (AI & MCP server interfaces)
├── metasploit/ (scripts, config, interaction layer)
├── tests/
├── codex-agent-c7.py
├── codex.yaml
├── Dockerfile
├── README.md
└── pyproject.toml
```

---

## 🧪 Example Zero-Day Validation Flow

1. Hacker sends exploit PoC and target fingerprint
2. AI launches sandbox sim via LXD with service running
3. Exploit code is executed
4. AI confirms effect (e.g. reverse shell, data leak, crash)
5. If verified, triggers crypto payment via Lightning or EVM-compatible chain
6. Adds report to ledger & notifies admin

---

## 🧾 Notes

- Project is designed to be extensible. Future features include swarm coordination and cloud bursting.
- Admin dashboard will later be added for monitoring, auto-deployment, and audit trails.

---

© 2025 Presient Solutions. All rights reserved.
