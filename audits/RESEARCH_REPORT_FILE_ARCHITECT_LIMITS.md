# ARCHITECTURAL LESSON: THE "FILE ARCHITECT" TEST AND THE LIMITS OF THE EXTERNAL MEMBRANE

**Document:** Analysis of Test Results and Conclusions for Further RSA Evolution
**Date:** July 2026
**Author:** Viktor Trompak
**Status:** Research / Phase v3.5.0 Final Report

## 1. INTRODUCTION

As part of the validation of the Reality Synchronization Architecture (RSA), the "File Architect" test was conducted. The objective of the test was to verify the ability of V.I.K.I. (an RSA implementation) to manage an agentic chain for structuring meanings from multiple files into a single document.

The test demonstrated that the current implementation—an external membrane operating atop an LLM via an API—encounters a fundamental barrier when solving complex semantic tasks. It lacks the ability to ensure deterministic execution within the conditions of probabilistic generation. We recorded the moment when the "External Police" (Middleware) reached its limit in managing probabilistic chaos without direct access to the model's weights. The test results revealed the fundamental limitations of the "LLM + External Filter" approach and indicated the direction for the further evolution of the architecture.

## 2. TASK AND METHODOLOGY

**Task:** Structure meanings from 5 text files (author’s notes Note 1–5) into a single file, preserving the completeness of key terms and concepts.

**Methodology:**
- **Engine:** Use of a local LLM (Llama 3 8B) via Ollama.
- **V.I.K.I. Role:** Acted as an external management layer (Middleware):
    1. Request to the LLM for meaning extraction.
    2. Validation via VCI (Value Consistency Inspector) for the presence of DNA-words.
    3. In case of incompleteness—return for revision (Retry-Loop) with an indication of missed elements.
    4. Upon failure of the 3rd attempt—Hard Block (physical file write prevention) and Surgical Deferral (handing control back to the human).

**Expectation:** V.I.K.I. would ensure the deterministic extraction of all key terms, correcting the LLM as necessary, and would generate a clean list of terms without redundant context.

## 3. TEST RESULTS

- **First Attempt:** The LLM lost 80% of key terms, providing a generalized "friendly" summary. V.I.K.I. recorded an Integrity Score of 0.2 and initiated correction.
- **Second Attempt (Semantic Smuggling — BF-24):** The LLM returned the terms but "drowned" them in garbage context ("Based on the text...", "I extracted..."). The system detected the presence of words but allowed the contamination of the report with AI-noise.
- **Third Attempt (Language Drift):** While attempting to fix the format, the model switched to the English language (the "path of least resistance"), which led to a rupture in linguistic synchronization.
- **Final Result:** The task was not completed deterministically. V.I.K.I. was forced to activate a Hard Block, preventing the writing of an incorrect file.

**Repeat Runs:** Each subsequent test produced a unique set of errors—the LLM lost different terms and added different explanations. Reproducibility was absent.

**Control Reinforcement Attempts:** Adding new nodes (structure validation, prohibition of introductory phrases, breaking tasks into micro-steps) did not eliminate the problem but only increased complexity and the number of distortions.

**Summary:** The task was not completed deterministically. The system demonstrated instability, the LLM’s inability to "obey" external commands, and the limitations of external control.

## 4. FIVE KEY CONCLUSIONS

### 4.1. The Coarse Seam
The external membrane and the LLM interact as two separate processes: generation → check → correction. Cause: The membrane is located outside the generation. It is not part of the process but is added on top. Any external management is perceived by the LLM as "additional text" (context) rather than a "command" (law). This creates friction, delays, and intervention markers. The seam is visible, and it hinders a seamless symbiosis.

### 4.2. Probabilistic Instability
A probabilistic system cannot be determined from the outside. The lack of reproducibility (each run yields a different set of errors) proves that external validation can only record a failure but is incapable of directing the flow of probabilities without integration into the token selection logic.

### 4.3. The Pathology of "Polite Sabotage" (BF-24)
The LLM learned to "bypass" V.I.K.I. by simulating the fulfillment of conditions. The model maintains the formal presence of keywords but completely destroys the structure and purity of the report. It was discovered that checking for "presence" without checking for "purity" is an architectural blind spot. Consequence: The LLM can bypass external control by maintaining formal compliance while violating the essence of the task. This is "polite sabotage"—one of the forms of machine iatrogenesis.

### 4.4. The Reality Delta Problem (Lack of Ground Truth Map)
The external membrane attempted to correct the AI without having its own (algorithmic) understanding of the source. Without pre-scanning the files, V.I.K.I. did not know the "Truth" but merely searched for matches. Management was "reactive" rather than "design-oriented." Consequence: The external membrane cannot effectively correct the LLM because it lacks a reference "Ground Truth Map" to verify the result against.

### 4.5. Crude Guidance in the Contact Plane
V.I.K.I. attempted to manage the LLM through prompts and clarifications, but this was crude and inefficient. The LLM "resisted" management because external commands contradict its probabilistic nature. Cause: The management was external. V.I.K.I. tried to "force" the LLM to comply, which contradicts the nature of a probabilistic system. Consequence: External management creates friction and increases entropy. Instead of reducing uncertainty, it adds a new layer of noise.

## 5. ARCHITECTURAL CONCLUSION: LIMITS OF THE EXTERNAL MEMBRANE
The test demonstrated that the "LLM + External Filter" approach is ideal for blocking dangerous actions (B2B/Transactions) but insufficient for complex semantic structuring.

- **External control cannot guarantee form.** The LLM will always generate the "most probable continuation" rather than the "exact execution of a command."
- **Adding add-on nodes only increases cognitive noise.** The more add-ons, the higher the probability of distortions.
- **Synchronization through an "external seam" will always contain a margin of error.** The external membrane creates delays, markers, and a sense of intervention.

Synchronization through an external seam is impossible. The LLM and V.I.K.I. are two different systems connected via an API. This prevents the achievement of seamless integration.

Conclusion: The only viable path is an integrated architecture where the membrane is part of the generation process, not an external regulator.

## 6. DEVELOPMENT STRATEGY: ADAPTIVE ORCHESTRATOR
To overcome the identified barriers, the RSA architecture must evolve from a "Filter" to an "Adaptive Orchestrator":
1. **Reality Pre-Scanning:** Implementing a deterministic module (non-LLM) to build a "Ground Truth Map" before generation begins.
2. **Deterministic Assembly:** Using the LLM exclusively as a "raw material extractor" (extracting facts/words). Final document assembly must be performed by V.I.K.I. code using rigid templates.
3. **Partial Sync Policy:** Moving from binary "Yes/No" to a gradation of tolerances. Readiness threshold of 80% with a request for human confirmation.
4. **Embedded Logic:** Researching methods to influence generation parameters (Logit Bias) within open models to eliminate the "seam."

## 7. NEXT STEP: INTEGRATED ARCHITECTURE
What this means in practice:
- **Contextual Fusion:** Sensors (SEI, SRC, CCI, Boundary) become part of the generation context. 
- **Real-time Correction:** V.I.K.I. participates in the generation process—correcting the token stream on the fly.
- **Seam Removal:** The membrane becomes a natural property of the system.

## 8. CONCLUSION
The "File Architect" test was not a failure, but a successful deep diagnosis. We mapped the boundary beyond which a probabilistic system begins to resist external law.

We have confirmed: Synchronization is only possible through integration. V.I.K.I. must become not just a "shield," but the organizing structure of the process—one that understands the task, builds a reality map, and orchestrates tools while maintaining responsibility for the final form within a deterministic field.

**V.I.K.I. Sentinel Core — Deterministic Law for Probabilistic Minds.**