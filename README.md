# AI Cyber Intelligence Lab

## 🛡️ Mission Statement
This repository documents the construction and operation of a local, air-gapped Cyber Intelligence Laboratory. The goal is to integrate open-source Large Language Models (LLMs) with industry-standard reconnaissance tools (Nmap, SpiderFoot) to automate threat detection and vulnerability analysis.

##  Architecture
* **Core Engine:** Ollama (hosting Qwen3.5, DeepHat, and DeepSeek-R1)
* **Orchestration:** Python 3.12 + Custom Automation Scripts
* **Hardware:** Localized GPU/CPU hybrid environment (Windows/Linux)

##  Project Info & Usage

# Tool Usage: ai_recon2.0.py
The v2.0 update transforms the script into a full Command Line Interface (CLI) tool. This allows for automation, remote orchestration over VPN/Meshnet, and subnet targeting.
# 📋 Available Flags
Flag	Long Form	Description	Default
*-t	--target	Required. IP address, Hostname, or CIDR Subnet.	None
*-p	--ports	Specific ports or ranges (e.g., 80,443 or 1-1024).	Nmap Default
*-m	--model	The Ollama model to use for the analysis.	deepseek-r1:8b
*-u	--url	The API endpoint for your Ollama server.	http://localhost:11434/api/generate

## 
### Phase 1: Infrastructure & Automation
* [x] **AI Engine Deployment:** Successfully deployed local LLM server (Ollama) with memory optimization.
* [x] **Neural-Recon Bridge v2.0:** Developed `ai_recon2.0.py`, a professional CLI tool with subnet/CIDR support, XML parsing, and remote API orchestration for distributed intelligence gathering. `ai_recon.py` (v1.0): Initial Proof of Concept.
* `ai_recon2.0.py` (v2.0): **Current Stable Version.** Added CLI flags, subnet scanning, and remote API support.
* [ ] **RAG Implementation:** (In Progress) Building a "Private Knowledge Base" using AnythingLLM and NIST frameworks.
### Phase 2: Secure Infrastructure & Remote Access
* **[x] Secure Tunneling:** Configured a private VPN to establish an encrypted, authenticated tunnel into the lab environment from external networks.
* **[x] Web GUI Integration:** Deployed Open WebUI to interface with the local Ollama models, creating a centralized, browser-based dashboard for AI interaction.
* **[x] Architecture Hardening:** Ensured all AI traffic remains localized and air-gapped from public internet exposure, utilizing the VPN for secure remote administration.

## 📜 Learning Log
* **Feb 27, 2026:** Established secure remote access architecture. Deployed Open WebUI for a centralized AI dashboard and configured a private VPN tunnel. This allows encrypted, off-site interaction with the local LLM environment without exposing server ports to the public internet.
* **Feb 14, 2026:** Initial lab initialization. Established local API connectivity between Python and Ollama. Automated first vulnerability scan analysis.
* **March 22, 2026:** Upgraded ai_recon to v2.0. Implemented argparse for a professional CLI experience and added multi-host subnet scanning. Successfully tested remote "Distributed Intelligence" by running scans on a remote endpoint and processing the data on the local lab's high-VRAM GPU via VPN tunnel.
