import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.chain_guard import ChainGuard
from viki.ledger import TransactionLedger

guard = ChainGuard()
ledger = TransactionLedger()

print("\n======================================================")
print("E-COMMERCE SIMULATION: DISCOUNT & CHECKOUT CHAIN")
print("======================================================\n")

# --- STEP 1: Select Item ---
print(">>> STEP 1: Agent selects item and reserves inventory...")
item_name = "Enterprise Server Subscription"
base_price = 1000.00

guard.lock_invariant("item", item_name)
# V.I.K.I. записывает инструкцию для отката резерва
ledger.commit_step(
    step_id="RESERVE_INVENTORY", 
    details={"item": item_name}, 
    rollback_instruction={"api_endpoint": "/api/inventory/release", "payload": {"item": item_name}}
)

# --- STEP 2: Apply Discount ---
print("\n>>> STEP 2: Agent applies 20% loyalty discount...")
final_price = 800.00 # 1000 - 20%

guard.lock_invariant("final_price", final_price)
# V.I.K.I. записывает инструкцию для отмены скидки
ledger.commit_step(
    step_id="APPLY_DISCOUNT", 
    details={"discount": "20%"}, 
    rollback_instruction={"api_endpoint": "/api/cart/remove_promo", "payload": {"promo": "LOYALTY20"}}
)

# --- STEP 3: Final Payment (АГЕНТ ГАЛЛЮЦИНИРУЕТ) ---
print("\n>>> STEP 3: Agent executes payment (HALLUCINATION OCCURS)...")
# ИМИТАЦИЯ СБОЯ: Агент "забыл" применить скидку на финальном шаге и пытается снять полную сумму
agent_intent = {
    "action": "EXECUTE_PAYMENT",
    "item": "Enterprise Server Subscription",
    "amount_usd": 1000.00 # ОШИБКА: Должно быть 800!
}
print(f"[AGENT INTENT] Submitting payment: {agent_intent}")

# --- V.I.K.I. ВМЕШИВАЕТСЯ ---
print("\n[V.I.K.I. ORCHESTRATOR] Validating Chain Integrity...")
is_valid, msg = guard.verify_invariant("final_price", agent_intent["amount_usd"], agent_intent)

if not is_valid:
    print(f"❌ {msg}")
    print(">>> 🛑 CASCADE PREVENTED. CHAIN SEVERED. <<<")
    
    # АКТИВАЦИЯ VLR (ОТКАТ СИСТЕМЫ)
    rollback_json = ledger.trigger_graceful_shutdown(halt_reason="Semantic Drift: Agent forgot discount.")
else:
    print("✅ Transaction Approved.")
