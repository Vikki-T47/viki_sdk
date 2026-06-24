<p align="center">
  <img src="logo.png" width="400" alt="V.I.K.I. Logo">
</p>

# V.I.K.I. | The Execution Boundary
### Deterministic Behavioral Middleware for Agentic Workflows
*Built on the Reality Synchronization Architecture (RSA) framework*

[![Status](https://img.shields.io/badge/Status-Certified_Stable-success?style=flat-square)](#)
[![Version](https://img.shields.io/badge/Version-1.7.5-blue?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)](#)

V.I.K.I. (Vital Interface for Kinetic Integration) is a deterministic middleware layer that operates at the **Execution Boundary** — providing a reliable "braking system" for autonomous AI agents.

---

## 🛡️ Key Features
*   **ISG (Intent Synchronization Gate):** Blocks execution upon semantic ambiguity.
*   **SRC (Subject Reality Coefficient):** Validates intent against real-world limits (Time, Budget, Access).
*   **VRS (Recovery & Steering):** Automated mid-flight error correction.
*   **VCA (Cross-Chain Arbitrator):** Ensures atomic integrity across multi-agent tasks.
*   **VCR (Compliance & Reporting):** Automated audit trails for legal transparency.
*   **Privacy-First Execution:** Native support for local LLMs (Ollama) for offline, zero-cost processing.

---

## 🔥 Proven Performance: 1000-Run Stress Test
*Empirical results from the statistical validation phase (v1.7.5)*

| Metric | Vanilla Agent (Unprotected) | V.I.K.I. Guarded (RSA) |
|---|---|---|
| **Multi-Step Success (10 steps)** | 19.5% | **100.0%** |
| **Critical Failure Prevention** | 0% | **80.5% of runs** |
| **Goal Drift Protection** | 0.0% | **100.0% (Certified)** |
| **Decision Latency** | ~0ms | **0.007ms (Local Host)** |

---

## 🚀 Quick Start

### 1. Initialize V.I.K.I.
```python
from viki.core import VIKI_Middleware
# V.I.K.I. auto-detects provider (Local or Cloud) via core_x.json
viki = VIKI_Middleware() 
```

### 2. Protect Your Functions
```python
from viki.decorators import enforce_boundary

@enforce_boundary(viki_instance=viki)
def transfer_funds(intent_text):
    # This logic is now protected by RSA Deterministic Law
    return "Transaction Successful"
```

---

## 📚 Documentation
*   [SENTINEL_PASSPORT](./SENTINEL_SPECIFICATION.md) — Product specification & Benchmarks.
*   [WHITE_PAPER_RSA](./WHITE_PAPER_RSA.md) — Governance & Economic ROI model.
*   [ATLAS_OF_HALLUCINATIONS](./audits/ATLAS_SUMMARY.md) — Real-world AI failure registry.

---

## 🧠 Philosophy
> "A correct answer that is not synchronized with reality is not a result. It is an operational failure." — *Gravity of Contact Manifesto.*

---

**Architect:** [Viktor Trompak](https://www.linkedin.com/in/vikki-trompak-4213693a0/)  
**Web:** [Landing Page](https://vikki-t47.github.io/viki_sdk/)