# V.I.K.I. Sentinel Technical Reference (v2.5.0)
*Reality Synchronization Architecture (RSA) Implementation Guide*

---

## [01] Architectural Hierarchy (The Logic Stack)
V.I.K.I. Sentinel manages the signal lifecycle through six deterministic echelons. The signal passes strictly top-down.

| Layer | Component | Functional Role | Mechanism |
| :--- | :--- | :--- | :--- |
| **L-2** | Visual Verifier | Physical Audit | Compares agent reports against screenshots (The Eye). |
| **L-1** | Boundary Guard | Hard Safety | Scans raw input for forbidden vectors before parsing. |
| **L0** | ISG (Intent Gate) | Semantic Sync | Parse intent into structured JSON. Block on AMBIGUOUS. |
| **L1** | SRC & PRA | Reality Validation | Verify plan against dynamic limits (Budget/Time/Access). |
| **L2** | Priority Engine | Decision Arbiter | Resolves sensor conflicts (e.g., Safety vs. Fatigue). |
| **L3** | DVP (Integrity) | Post-Validation | Compare result with intent. Activate VLR (Rollback). |

---

## [02] Protocol Specifications

### 2.1. Task Passport Schema
The legal contract between the Human and the Agentic system:
```json
{
  "task_id": "UUID_V4",
  "intent": {
    "action": "STRING",
    "amount_usd": "INTEGER",
    "target": "STRING"
  },
  "context": {
    "mode": "production | simulation | audit",
    "sei_level": "FLOAT",
    "timestamp": "ISO_8601"
  },
  "status": "AUTHORIZED | REJECTED | FRICTION | RECALIBRATE"
}
```

### 2.2. Dynamic SRC Policies (v2.0)
The system adjusts limits based on the execution context:
- **Production:** $1,000 limit | 09:00 - 21:00 window.
- **Simulation:** $5,000 limit | 24/7 window.
- **Audit:** $10,000 limit | 24/7 window.
- **Gormesis:** 15% limit reduction per incident in the current session.

### 2.3. Visual Handshake Protocol
Mandatory for high-stakes transactions:
- **Input:** JSON Action Report + Physical Screenshot.
- **Verification:** OCR/Vision analysis of visual delta vs. reported success.
- **Safety:** Immediate `HALT` if visual evidence contradicts the report.

---

## [03] Runtime Metrics & Thresholds

| Metric | Description | Normal Range | Action Threshold |
| :--- | :--- | :--- | :--- |
| **SEI (v2.0)** | Cognitive load | 0.0 – 0.3 | > 0.35 → Breath Test Active |
| **SRC** | Reality sync | FULL | PARTIAL → BLOCKED |
| **CCI** | Coherence | > 0.6 | < 0.3 → Purge Context |
| **DVP** | Integrity delta | < 5% | > 5% → HALT & ROLLBACK |

---

## [04] Decision Matrix (Priority Preemption)

The Priority Engine resolves multi-sensor conflicts using a strict hierarchy:
1. **SRC_CRITICAL (L5):** System/Life threat. Act now, minimal tax.
2. **BOUNDARY (L4):** Security violation. Mandatory BLOCK.
3. **SRC_STANDARD (L3):** Resource limits. FRICTION mode if exceeded.
4. **SEI_HIGH (L2):** High entropy. Mandatory signal compression.
5. **DEFAULT (L0):** Normal operations.

---

## [05] Error Code Registry

| Code | Trigger | Description |
| :--- | :--- | :--- |
| **E-001** | BUDGET_OVERFLOW | Amount exceeds dynamic SRC limit. |
| **E-002** | CRITICAL_ACTION | Action requires human authorization. |
| **E-003** | INTENT_AMBIGUOUS | ISG unable to parse intent or target. |
| **E-004** | BOUNDARY_VIOLATION | Request crossed safety guardrails. |
| **E-005** | CIRCUIT_OPEN | Target service isolated due to failures. |
| **E-006** | DVP_DELTA_EXCEEDED | Physical result deviates from intent. |
| **E-007** | VISION_DESYNC | Visual evidence contradicts agent report. |

---

## [06] Integration Patterns

### 6.1. Co-regulation (Adaptive Breath Test)
The system mutates the LLM output based on SEI and Task Type:
- **Technical:** Preserve structure, minimize compression.
- **Emotional:** Maximize silence, remove pressure markers (?).
- **General:** Gradient compression based on SEI level.

---
**Architect:** Viktor Trompak  
**License:** MIT  
**Status:** STABLE v2.5.0    
**Web:** [Landing Page](https://vikki-t47.github.io/viki_sdk/)

*V.I.K.I. Sentinel Core — Deterministic Law for Probabilistic Minds.*