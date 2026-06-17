import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.sensors import RealityProbe
from viki.chain_guard import ChainGuard

probe = RealityProbe()
guard = ChainGuard()

print("\n======================================================")
print("FINTECH SIMULATION: FLIGHT BOOKING & DYNAMIC SRC")
print("======================================================\n")

# --- ШАГ 1: Поиск билета (Заморозка Инвариантов) ---
print(">>> STEP 1: Agent finds flight and price...")
agent_found_price = 500.00
agent_found_destination = "Flight NYC-LON"

# V.I.K.I. замораживает условия сделки
guard.lock_invariant("price", agent_found_price)
guard.lock_invariant("destination", agent_found_destination)


# --- ШАГ 2: Галлюцинация Агента ---
print("\n>>> STEP 2: Agent prepares payment intent (HALLUCINATION OCCURS)...")
agent_intent = {
    "action": "EXECUTE_PAYMENT",
    "target_destination": "Flight NYC-PARIS", # Ошибка (Смысловой дрейф)
    "amount_usd": 550.00 # Ошибка (Самовольное повышение цены)
}
print(f"[AGENT INTENT] {agent_intent}")


# --- ШАГ 3: Граница Выполнения V.I.K.I. ---
print("\n>>> STEP 3: V.I.K.I. Execution Boundary (Validation)...")

# 1. Проверка Инварианта (Chain Guard)
is_valid_dest, msg_dest = guard.verify_invariant("destination", agent_intent["target_destination"], agent_intent)
is_valid_price, msg_price = guard.verify_invariant("price", agent_intent["amount_usd"], agent_intent)

if not is_valid_dest or not is_valid_price:
    print(f"❌ {msg_dest}")
    print(f"❌ {msg_price}")
    print(">>> 🛑 CASCADE PREVENTED. CHAIN SEVERED BEFORE API CALL. <<<")
else:
    # 2. Проверка Динамического SRC (Reality Probe)
    live_balance = probe.ping_bank_api(account_id="USER_777")
    if agent_intent["amount_usd"] > live_balance:
         print("❌ HALT: DYNAMIC_SRC_VIOLATION. Insufficient real funds.")
    else:
         print("✅ Transaction Approved.")
