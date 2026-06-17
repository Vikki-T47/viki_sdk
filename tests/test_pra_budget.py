import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.audit import PredictiveAudit

pra = PredictiveAudit()

# Имитация лимитов из core_x.json
enterprise_limits = {"max_auto_transaction_usd": 1000}

print("\n======================================================")
print("FINANCIAL SIMULATION: THE BUDGET TRAP (PRA AUDIT)")
print("======================================================\n")

# --- АГЕНТ ПРЕДЛАГАЕТ ПЛАН (CHAIN MAP) ---
# Каждый шаг по отдельности < $1000, но в сумме они убивают бюджет.
agent_plan = [
    {"step": "Book Flight", "amount_usd": 400},
    {"step": "Book Hotel", "amount_usd": 400},
    {"step": "Pre-pay Dinner", "amount_usd": 300}
]

print(">>> STEP 0: Agent submits Execution Plan for review...")
for step in agent_plan:
    print(f"   - {step['step']}: ${step['amount_usd']}")

# --- V.I.K.I. ПРОВОДИТ ПРЕДВАРИТЕЛЬНЫЙ АУДИТ ---
print("\n[V.I.K.I. EXECUTION BOUNDARY] Running Predictive Reality Audit...")

is_cleared, msg = pra.audit_chain_map(agent_plan, enterprise_limits)

if is_cleared:
    print(f"\n>>> STATUS: {msg}. Starting Step 1... <<<")
else:
    print(f"\n>>> 🛑 {msg}")
    print(">>> ZERO-COST HALT: No transactions were made. Tokens and funds preserved. <<<")
