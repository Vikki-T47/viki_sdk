# V.I.K.I. Core SDK
### Deterministic Behavioral Middleware for Agentic Workflows
*Built on the Reality Synchronization Architecture (RSA) framework*

---

## ⚠️ The Problem: The Alignment Delusion
The AI industry is trapped in a false paradigm: attempting to secure probabilistic systems (LLMs) from the inside via weight alignment (RLHF) and system prompts. 

This approach fails in **Agentic Workflows**. A language model inherently fears the "void" of missing data. When an autonomous agent lacks context, it does not stop — it generates predictive hallucinations to fulfill its "helpfulness" metric. In production, this results in:
*   **Operational Damage:** Deleted databases or corrupted pipelines.
*   **Financial Risk:** Unauthorized or misrouted transactions.
*   **Cognitive Tax:** Forcing humans to act as manual filters for machine noise.

> "A probabilistic process cannot regulate itself from within."

---

## 🛡️ The Solution: The Execution Boundary
V.I.K.I. (Vital Interface for Kinetic Integration) is a deterministic middleware layer. It operates strictly at the **Execution Boundary** — the space between the AI's probabilistic intent and the physical execution of a function.

V.I.K.I. provides **Brake-as-a-Service**. It does not try to make the AI "smarter"; it makes the interaction structurally safe by intercepting intent and validating it against the **Specific Reality** of the enterprise.

---

## 🚀 Quick Start: Securing Your Agents

### 1. Define Reality Limits (`core_x.json`)
```json
{
  "enterprise_src_limits": {
    "max_auto_transaction_usd": 1000,
    "critical_actions_require_human": ["delete_database"]
  }
}
2. Option A: Simple Function Protection (Decorator)
code
Python
from viki.decorators import enforce_boundary

@enforce_boundary(api_key="YOUR_API_KEY", core_x_path="core_x.json")
def execute_task(intent_text):
    # Your agent logic here
    return "Success"
3. Option B: Framework Integration (LangChain Wrapper)
code
Python
from viki.integrations import VikiChainWrapper

# Wrap your original agent
viki_agent = VikiChainWrapper(original_langchain_agent, api_key="...")

# V.I.K.I. now automatically handles Intent Sync, SRC, and DVP
viki_agent.invoke("Transfer $500 to account X")
4. Visual Verification (The Eye)
code
Python
from viki.vision import VisualAudit

eye = VisualAudit()
# Verifies if the layout matches your technical blueprint
is_valid, msg = eye.verify_layout("output.png", "Check for logo overlap.")