# AI Cyber Intelligence Lab

## 🛡️ Mission Statement
This repository documents the construction and operation of a local, air-gapped Cyber Intelligence Laboratory. The goal is to integrate open-source Large Language Models (LLMs) with industry-standard reconnaissance tools (Nmap, SpiderFoot) to automate threat detection and vulnerability analysis.

## 🏗️ Architecture
* **Core Engine:** Ollama (hosting DeepSeek-R1 / Llama3)
* **Orchestration:** Python 3.12 + Custom Automation Scripts
* **Hardware:** Localized GPU/CPU hybrid environment (Windows/Linux)

## 📂 Project Modules

### Phase 1: Infrastructure & Automation
* **[x] AI Engine Deployment:** Successfully deployed local LLM server (Ollama) with memory optimization.
* [x] Neural-Recon Bridge v2.0: Developed ai_recon2.0.py, a professional CLI tool with subnet/CIDR support, XML parsing, and remote API orchestration for distributed intelligence gathering.
* **[ ] RAG Implementation:** (In Progress) Building a "Private Knowledge Base" using AnythingLLM and NIST frameworks.
### Phase 2: Secure Infrastructure & Remote Access
* **[x] Secure Tunneling:** Configured a private VPN to establish an encrypted, authenticated tunnel into the lab environment from external networks.
* **[x] Web GUI Integration:** Deployed Open WebUI to interface with the local Ollama models, creating a centralized, browser-based dashboard for AI interaction.
* **[x] Architecture Hardening:** Ensured all AI traffic remains localized and air-gapped from public internet exposure, utilizing the VPN for secure remote administration.

## 📜 Learning Log
* **Feb 27, 2026:** Established secure remote access architecture. Deployed Open WebUI for a centralized AI dashboard and configured a private VPN tunnel. This allows encrypted, off-site interaction with the local LLM environment without exposing server ports to the public internet.
* **Feb 14, 2026:** Initial lab initialization. Established local API connectivity between Python and Ollama. Automated first vulnerability scan analysis.
* **March 22, 2026:** Upgraded ai_recon to v2.0. Implemented argparse for a professional CLI experience and added multi-host subnet scanning. Successfully tested remote "Distributed Intelligence" by running scans on a remote endpoint and processing the data on the local lab's high-VRAM GPU via VPN tunnel.
