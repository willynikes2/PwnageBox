# 📦 PWNAGEBOX — Unified PRD & SRS

---

## 🧠 Project Name
**PwnageBox: Autonomous AI Cybersecurity Platform**

## 📅 Version
v1.0  
Date: July 18, 2025  
Author: Presient Labs

---

## 📌 Executive Summary

PwnageBox is a plug-and-pwn AI-powered cybersecurity device designed to autonomously scan, exploit, and report on vulnerabilities in any target environment — digital or human. It uses multiple radios (WiFi, Bluetooth, Zigbee, SDR, etc.) to map and interact with the surrounding attack surface, then deploys three agentic AI modules:

- **Scammer**: Recon + device fingerprinting
- **Researcher**: Exploit reasoning + 0-day discovery
- **Pwner**: Goal-driven exploit executor

In Enterprise mode, the box is deployed by a field agent (technical or not) and left on-site. It autonomously performs its functions and emails a full vulnerability report to clients at the end of the day.

A dedicated **Social Engineering Module** augments attacks with AI-generated pretexts and voice cloning to test human-layer security and trust models.

---

## 🎯 Product Goals

- Scan and exploit with no user input
- Work offline or sync with a cloud-based command hub
- Be deployable by non-technical field agents
- Enable red/blue team assessments, patching, or silent persistence
- Deliver clear reports to stakeholders automatically
- Include human-layer (social) testing via AI-generated attacks

---

## 🧩 Core System Modules

### 1. Scammer (Recon AI)
- Multi-radio scanning (WiFi, Zigbee, BLE, SDR)
- OS/service fingerprinting
- Firmware version and vendor mapping
- MAC signal tracking
- Output: Structured device fingerprint database

### 2. Researcher (Exploit Reasoning AI)
- Matches fingerprints to CVEs using Vulners/NVD/ExploitDB
- Ranks exploit probability
- Tags targets as patchable, vulnerable, or persistent candidates
- Contains Zero-Day Discovery Pipeline:
  - Decompilation (Ghidra, Binary Ninja, Cutter)
  - Static analysis (CodeQL + GPT)
  - Symbolic execution (angr)
  - Fuzzing (AFL++, Boofuzz)
  - GPT-guided exploit synthesis

### 3. Pwner (Agentic Exploit Engine)
- Executes chosen exploits via metasploit-style interface
- Selects execution goals: Patch, Persist, Report, or Observe
- Backdoor injection and credential theft
- Logs outcomes per target

---

## 🗣️ 4. Social Engineering Module: `voicepwner`
- Voice cloning using LLM TTS models (ElevenLabs, Coqui, Bark)
- GPT-4o/Claude generates phone/email pretexts (CEO voice, fake IT calls, etc.)
- Voice playback scripts executed via phone, SIP, or Slack bot
- Logs response outcome, triggers, and trust levels

---

## 💻 User Interaction

### Admin/Hacker
- Maintains exploit DB
- Pushes updates to boxes via Git or REST API
- Monitors device syncs and activation

### Field Agent
- Plugs in box (WiFi auto-connect or fallback AP mode)
- No CLI or setup required
- Reports auto-sent to client email or S3 bucket

### Client
- Receives encrypted report PDF or secure portal link
- Report includes summary, vulnerabilities, fixes, and human-layer test results

---

## 📦 Hardware Specification (MVP)

| Component         | Model / Notes                                 |
|------------------|-----------------------------------------------|
| Compute Core     | Raspberry Pi 5 or Jetson Orin Nano             |
| Storage          | 512GB–1TB SSD (USB 3.0 or onboard NVMe)       |
| WiFi Adapters    | Alfa AWUS036ACH + Panda PAU09                 |
| Bluetooth        | ASUS BT500                                     |
| Zigbee           | ConBee II                                      |
| Z-Wave           | Aeotec Z-Stick 7                               |
| SDR              | HackRF One or RTL-SDR Blog V3                  |
| Power Supply     | USB-C 45W PD bank or AC adapter                |
| Interface        | Web GUI only (http://pwnagebox.local)          |
| Optional Display | eInk or HDMI touch panel (for branding/demo)  |

---

## 🔁 Deployment Modes

| Mode        | Behavior                                                   |
|-------------|------------------------------------------------------------|
| Audit       | Recon + report only                                        |
| Pentest     | Exploits + remediation suggestions                         |
| Red Team    | Full exploit + optional persistence + human trust attack   |
| SE Only     | Run only social engineering module                         |
| Zero Day    | Enable deep binary analysis and fuzzing                    |

All modes are controlled by license keys and signed activation policies.

---

## 🧾 Reporting System

- Markdown → HTML → PDF export
- Encrypted ZIP emailed to:
  - Field agent
  - Client
  - Admin (optional)
- Includes:
  - Device map
  - Vulnerability details
  - Exploits used
  - Fix suggestions
  - Trust test outcomes
  - CVSS scoring + risk matrix

---

## 🗄️ Directory Structure

