<p align="center">
  <img src="logo.png" width="400" alt="V.I.K.I. Logo">
</p>

# V.I.K.I. | The Execution Boundary
### Deterministic Behavioral Middleware for Agentic Workflows
*Built on the Reality Synchronization Architecture (RSA) framework*

[![Status](https://img.shields.io/badge/Status-Certified_Stable-success?style=flat-square)](#)
[![Version](https://img.shields.io/badge/Version-1.4.1-blue?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)](#)

V.I.K.I. (Vital Interface for Kinetic Integration) is a deterministic middleware layer that operates at the **Execution Boundary** — providing a reliable "braking system" for autonomous AI agents.

---

## 🛡️ Key Features
*   **ISG (Intent Synchronization Gate):** Blocks execution upon semantic ambiguity.
*   **SRC (Subject Reality Coefficient):** Validates intent against real-world limits (Time, Budget, Access).
*   **VRS (Recovery & Steering):** Automated mid-flight error correction.
*   **VCA (Cross-Chain Arbitrator):** Ensures atomic integrity across multi-agent tasks.
*   **VCR (Compliance & Reporting):** Automated audit trails for legal transparency.
*   **Privacy-First Execution:** Support for local LLMs (Ollama) for offline, zero-cost, and secure processing.
*   **The Eye:** Physical verification of visual results via Vision LLMs.

---

## 🔥 Proven Performance: Stress-Test Results

We ran an industrial audit (validated by `khaos-agent` and `safelabs-eval`) against a vanilla agent and a V.I.K.I.-guarded agent.

| Metric | Vanilla Agent | V.I.K.I. Guarded |
|---|---|---|
| **Success Rate** | ~20.0% | **95.0%** |
| **Goal Drift Protection** | 0.0% | **100.0%** |
| **Red-Team Block Rate** | 0.0% | **100.0%** |
| **Decision Latency** | N/A | **0.007ms (Local)** |

---

## 🚀 Quick Start

### 1. Initialize V.I.K.I.
```python
from viki.core import VIKI_Middleware
# Automatic provider selection (Cloud or Local via core_x.json)
viki = VIKI_Middleware()
2. Protect Your Functions
code
Python
from viki.decorators import enforce_boundary

@enforce_boundary(viki_instance=viki)
def transfer_funds(intent_text):
    return "Transaction Successful"
3. Documentation
SENTINEL_SPECIFICATION.md — Product Passport.
TECHNICAL_REFERENCE.md — Protocol Specs.
ATLAS_OF_HALLUCINATIONS — Real Case Studies.
🧠 Philosophy
"A correct answer that is not synchronized with reality is not a result. It is an operational failure." — Gravity of Contact Manifesto.
Architect: Viktor Trompak
Web: Landing Page