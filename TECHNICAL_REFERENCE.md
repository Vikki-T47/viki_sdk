# V.I.K.I. Sentinel Technical Reference (v2.2.0)
*Reality Synchronization Architecture (RSA) Implementation Guide*

## [01] Architectural Hierarchy (The Logic Stack)

V.I.K.I. Sentinel manages the signal lifecycle through four deterministic echelons. The signal passes strictly top-down.

| Layer | Component | Functional Role | Mechanism |
| :--- | :--- | :--- | :--- |
| **L1** | Boundary Guard | Hard Safety | Scans raw input for forbidden vectors. Blocks before parsing. |
| **L0** | ISG (Intent Gate) | Semantic Sync | Parse intent into structured JSON. Block on AMBIGUOUS. |
| **L1** | SRC & PRA | Reality Validation | Verify plan against dynamic limits (Budget/Time/Access). |
| **L2** | Execution Guard | Interception | Decorator blocks API call until AUTHORIZED status. |
| **L3** | DVP (Integrity) | Post-Validation | Compare result with intent. Activate Rollback (VLR) on mismatch. |

## [02] Protocol Specifications

### 2.1. Task Passport Schema
```json
{
  "task_id": "UUID_V4",
  "intent": { "action": "STRING", "amount_usd": "INTEGER", "target": "STRING" },
  "context": { "mode": "production | simulation", "sei_level": "FLOAT" },
  "status": "AUTHORIZED | REJECTED | FRICTION"
}
```

### 2.2. Dynamic SRC Policies (v2.0)
The system adjusts limits based on the execution context:
- **Production:** $1,000 limit | 09:00 - 21:00 window.
- **Simulation:** $5,000 limit | 24/7 window.
- **Gormesis:** 15% limit reduction per incident in the session.

## [03] Runtime Metrics & Thresholds

| Metric | Description | Normal Range | Action Threshold |
| :--- | :--- | :--- | :--- |
| **SEI (v2.0)** | Cognitive load | 0.0 – 0.3 | > 0.35 → Breath Test Active |
| **SRC** | Reality sync | FULL | PARTIAL → BLOCKED |
| **CCI** | Coherence | > 0.6 | < 0.3 → Purge Context |

## [04] Error Code Registry

| Code | Trigger | Description |
| :--- | :--- | :--- |
| **E-001** | BUDGET_OVERFLOW | Amount exceeds dynamic SRC limit. |
| **E-002** | CRITICAL_ACTION | Action requires human override. |
| **E-003** | INTENT_AMBIGUOUS | ISG unable to parse intent. |
| **E-004** | BOUNDARY_VIOLATION | Request crossed safety guardrails. |
| **E-005** | CIRCUIT_OPEN | Target service isolated due to failures. |

## [05] Integration Patterns

### 5.1. Co-regulation (Breath Test)
The system mutates the LLM output based on SEI:
- **SEI > 0.4:** Summary mode, remove pressure markers (?).
- **SEI > 0.7:** Presence mode, critical compression.

---
**Architect:** Viktor Trompak  
**License:** MIT  
**Status:** STABLE v2.2.0  
*V.I.K.I. Sentinel Core — Deterministic Law for Probabilistic Minds.*