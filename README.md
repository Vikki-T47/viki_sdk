<p align="center">
  <img src="logo.png" width="400" alt="V.I.K.I. Logo">
</p>

# V.I.K.I. | The Execution Boundary
### Deterministic Co-Regulation Middleware for Human-AI Symbiosis
*Built on the Reality Synchronization Architecture (RSA) framework*

[![Status](https://img.shields.io/badge/Status-Certified_Stable-success?style=flat-square)](#)
[![Version](https://img.shields.io/badge/Version-2.2.0-blue?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)](#)

V.I.K.I. (Vital Interface for Kinetic Integration) is a deterministic middleware layer that operates at the **Execution Boundary** — establishing an adaptive balance between Human and Artificial Intelligence.

---

## 🧬 Key Behavioral Features
*   **SEI v2.0 (Subject Entropy Index):** Multi-dimensional sensing of human cognitive load (Text + Time + Behavior).
*   **Adaptive Breath Test:** Gradient response compression that "breathes" in sync with the user's state and task context.
*   **Dynamic SRC Mapping:** Context-aware policies (Production/Simulation) and Gormesis-driven dynamic limits.
*   **Boundary Guard:** Deterministic "No" without biological mimicry or sycophancy.
*   **Cognitive Mirroring:** Subtle adjustment of linguistic density to match the user's pace.
*   **VCA (Cross-Chain Arbitrator):** Ensures atomic integrity and multi-agent synchronization.
*   **Privacy-First Execution:** Native support for local LLMs (Ollama) for zero-cost, air-gapped autonomy.

---

## 🔥 Performance: 1000-Run Stress Test
*Empirical results from the v2.2.0 validation phase*

| Metric | Vanilla Agent | V.I.K.I. Guarded |
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
# V.I.K.I. auto-detects provider and loads dynamic policies
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
*   [WHITE_PAPER_RSA](./WHITE_PAPER_RSA.md) — Strategy & ROI model.
*   [TECHNICAL_REFERENCE](./TECHNICAL_REFERENCE.md) — Full Protocol & Policy Specs.
*   [ATLAS_OF_HALLUCINATIONS](./audits/ATLAS_SUMMARY.md) — Real-world AI failure registry.

---

## 🧠 Philosophy
> "A correct answer that is not synchronized with reality is not a result. It is an operational failure." — *Gravity of Contact Manifesto.*

---

**Architect:** [Viktor Trompak](https://www.linkedin.com/in/vikki-trompak-4213693a0/)    
**Web:** [Landing Page](https://vikki-t47.github.io/viki_sdk/)