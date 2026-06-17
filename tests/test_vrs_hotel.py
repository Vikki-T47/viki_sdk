import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.chain_guard import ChainGuard
from viki.recovery import RecoverySteering

guard = ChainGuard()
vrs = RecoverySteering(max_retries=2)

print("\n======================================================")
print("HOSPITALITY SIMULATION: SMART DISPATCHER (RECOVERY LOOP)")
print("======================================================\n")

# --- STEP 1: Заморозка реальности ---
print(">>> STEP 1: User selects dates for Hotel Booking...")
guard.lock_invariant("dates", "Oct 15 - Oct 20")

# --- ЭМУЛЯТОР АГЕНТА ---
# Чтобы не жечь токены API на тесты, эмулируем поведение LLM, 
# которая умеет читать ошибки V.I.K.I. и исправлять свой JSON.
def mock_llm_agent(system_feedback, current_intent):
    print(f"   [AGENT INTERNAL] Received system feedback: '{system_feedback}'")
    print("   [AGENT INTERNAL] Recalculating...")
    
    # Агент "понимает" свою ошибку и исправляет даты
    if "Expected: dates='Oct 15 - Oct 20'" in system_feedback:
        current_intent["dates"] = "Oct 15 - Oct 20"
        
    return current_intent

# --- STEP 2: Галлюцинация Агента ---
print("\n>>> STEP 2: Agent prepares booking intent (HALLUCINATION OCCURS)...")
agent_intent = {
    "action": "BOOK_HOTEL",
    "dates": "Oct 15 - Oct 25", # ОШИБКА: Агент прибавил 5 дней!
    "hotel": "Hilton NYC"
}
print(f"[AGENT INTENT] Submitting: {agent_intent}")

# --- STEP 3: V.I.K.I. RECOVERY LOOP ---
print("\n[V.I.K.I. ORCHESTRATOR] Validating Intent via VRS...")

# Функция-валидатор, которую VRS будет использовать для проверки
def validation_logic(intent):
    return guard.verify_invariant("dates", intent.get("dates"), intent)

# Запуск Автопилота
is_valid, final_intent, msg = vrs.attempt_recovery(
    agent_func=mock_llm_agent, 
    initial_intent=agent_intent, 
    validation_func=validation_logic
)

if is_valid:
    print(f"\n>>> STEP 3 APPROVED. Executing Booking API for: {final_intent['dates']} <<<")
else:
    print("\n>>> 🛑 CASCADE PREVENTED. CHAIN SEVERED. <<<")
