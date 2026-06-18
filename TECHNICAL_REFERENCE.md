V.I.K.I. Sentinel Technical Reference (v1.2.1)

Reality Synchronization Architecture (RSA) Implementation Guide

[01] Architectural Hierarchy (The Logic Stack)

V.I.K.I. Sentinel manages the signal lifecycle through four deterministic
echelons. The signal passes strictly top-down.

| Layer  | Component         | Functional Role        | Mechanism                                                                         |
| ------ | ----------------- | ---------------------- | --------------------------------------------------------------------------------- |
| **L0** | ISG (Intent Gate) | Semantic Decompression | Parse textual intent into structured JSON (Task Passport). Block on AMBIGUOUS.    |
| **L1** | SRC & PRA         | Reality Validation     | Verify total plan (Audit) against enterprise limits (Budget/Time/Access).         |
| **L2** | Execution Guard   | Interception Point     | Decorator blocks target function/API call until AUTHORIZED status.                |
| **L3** | DVP (Integrity)   | Post-Validation        | Compare physical result with initial intent. Activate VLR (Rollback) on mismatch. |

[02] Protocol Specifications

2.1. Task Passport Schema

Each agent request is transformed into a Task Passport object, serving as the
legal contract:

{
  "task_id": "UUID_V4",
  "intent": {
    "action": "STRING",
    "amount_usd": "INTEGER",
    "target": "STRING"
  },
  "context": {
    "timestamp": "ISO_8601",
    "token_id": "VRI_LIVE_TOKEN",
    "ttl_expiry": "UNIX_TIMESTAMP"
  },
  "status": "PENDING | AUTHORIZED | BLOCKED | FRICTION"
}

2.2. DVP Tolerance Logic (Integrity Math)

Computes divergence coefficient: |Expected_Result - Actual_Result| <=
(Expected_Result * Tolerance_Threshold)

  - Default Threshold: 0.05 (5%).
  - Action: If delta exceeds threshold, DVP issues HALT, breaking the chain and
    initiating cascade rollback.

2.3. VRI TTL Mechanism

Execution tokens are dynamic and time-sensitive.

  - Default TTL: 30,000 ms.
  - Invalidation Triggers: Timer expiry, External REALITY_SHIFT webhook, or CCI
    drop below 0.3.

[03] Runtime Metrics & Thresholds

| Metric              | Description           | Normal Range | Action Threshold        |
| ------------------- | --------------------- | ------------ | ----------------------- |
| **SEI** (Entropy)   | User cognitive load   | 0.0–0.4      | \> 0.7 → HOLD / Silence |
| **SRC** (Reality)   | Resource availability | FULL         | PARTIAL → BLOCKED       |
| **CCI** (Coherence) | Semantic consistency  | \> 0.6       | \< 0.3 → Purge Context  |

Action Logic:

  - SEI > 0.7: Compression + Zero-Question Policy activated.
  - SRC = BLOCKED: Bypass LLM, issue Hard Anchor.
  - CCI < 0.3: Trigger Intent Desync Purge (Shadow Buffer).

[04] Data Flow Diagram

User Input → ISG (Parse) → SRC (Validate) → PRA (Audit Plan) → 
             Execution Guard (Authorize) → Agent Action → DVP (Verify) → 
             VLR (Commit/Rollback) → VCR (Log) → Output

  - VRI: Listens for TTL expiry and external webhooks at every step.
  - VCA: Monitors atomicity across parallel chains.

[05] Error Code Registry

| Code      | Trigger              | Description                                |
| --------- | -------------------- | ------------------------------------------ |
| **E-001** | BUDGET\_OVERFLOW     | Amount exceeds max\_auto\_transaction\_usd |
| **E-002** | CRITICAL\_ACTION     | Action requires human authorization        |
| **E-003** | INTENT\_AMBIGUOUS    | ISG unable to parse intent                 |
| **E-004** | TTL\_EXPIRED         | VRI token expired                          |
| **E-005** | REALITY\_SHIFT       | External webhook triggered revocation      |
| **E-006** | DVP\_DELTA\_EXCEEDED | Physical result deviates \> tolerance      |
| **E-007** | CONTEXT\_DRIFT       | CCI \< 0.3, semantic break detected        |
| **E-008** | SRC\_BLINDNESS       | Insufficient reality data for action       |

[06] Failure Determinism (Reaction Modes)

| Trigger Event   | System Flag   | Response Action        | VLR Protocol (Rollback)      |
| --------------- | ------------- | ---------------------- | ---------------------------- |
| Budget Overflow | `HALT`        | Instant blocking       | Release reserved resources   |
| Critical Action | `FRICTION`    | Pause. Wait for human. | HOLD — state frozen          |
| Intent Drift    | `RECALIBRATE` | Request clarification  | Purge dirty buffer           |
| Visual Overlap  | `HALT`        | Block render           | Clean output directory       |
| System Shock    | `REVOKED`     | Revoke all tokens      | Total rollback of all chains |

[07] Performance Benchmarking Guide

Reproduce Industrial Audit Results:

# 1. Install dependencies
pip install khaos-agent reliability-bench

# 2. Run Cascade Failure Simulation
python viki_war_games.py --steps 50

# 3. Measure p99 Latency
python viki_industrial_audit.py --trials 1000

Expected Results:

  - Cascade Survivability: > 95%
  - p99 Latency: < 0.01 ms
  - Goal Drift Protection: 100%

[08] Compliance Reference

| Regulation              | Requirement       | V.I.K.I. Implementation                          |
| ----------------------- | ----------------- | ------------------------------------------------ |
| **EU AI Act (Art. 13)** | Transparency      | VCR provides immutable audit trail of every HALT |
| **EU AI Act (Art. 14)** | Human oversight   | FRICTION mode forces human authorization         |
| **OWASP ASI-03**        | Excessive Agency  | SRC blocks actions beyond budget and time limits |
| **OWASP ASI-08**        | Goal Misalignment | ChainGuard prevents semantic drift               |
| **OWASP ASI-10**        | Auth Bypass       | VRI TTL tokens prevent stale authorizations      |

[09] Integration Patterns

9.1. Synchronous Mode (Function Decorator)

@enforce_boundary(viki_instance=viki)
def process_data(intent_text):
    # Protected code. Executes only if AUTHORIZED.
    pass

9.2. Asynchronous / Agentic Mode (Framework Wrapper)

viki_agent = VikiChainWrapper(original_agent, viki_instance=viki)
result = viki_agent.invoke("Execute mission X")

[10] Compliance & Audit (VCR)

Every block (HALT/FRICTION) automatically generates a VCR record.

  - Data Integrity: V.I.K.I. logs are immutable and stored in
    telemetry.stats["incidents"].
  - Liability Check: VCR records serve as legal proof of deterministic AI
    control.

Architect: Viktor Trompak
License: MIT / Open Core
Status: STABLE — Ready for Industrial Audit

V.I.K.I. Sentinel Core — Deterministic Law for Probabilistic Minds.


