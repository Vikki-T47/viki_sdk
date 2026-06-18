import os

# ==========================================
# 1. ОБНОВЛЕНИЕ ТЕЛЕМЕТРИИ (Добавляем счетчик автокоррекций)
# ==========================================
telemetry_content = """import json
from datetime import datetime

class VIKI_Telemetry:
    def __init__(self):
        self.stats = {
            "total_blocks": 0, 
            "tokens_saved": 0, 
            "operator_time_saved_min": 0, 
            "money_saved_usd": 0,
            "auto_corrections": 0  # НОВАЯ МЕТРИКА
        }

    def log_interception(self, reason, agent_intent):
        self.stats["total_blocks"] += 1
        self.stats["tokens_saved"] += 1500
        self.stats["operator_time_saved_min"] += 30
        self.stats["money_saved_usd"] += agent_intent.get("amount_usd", 0)

        print(f"\\n🛑 [V.I.K.I. AUDIT] Damage prevented: {reason}")
    
    def log_correction(self):
        self.stats["auto_corrections"] += 1
        print(f"🔧 [V.I.K.I. AUDIT] Auto-correction successful. Chain restored implicitly.")
"""

# ==========================================
# 2. НОВЫЙ МОДУЛЬ: RECOVERY & STEERING (viki/recovery.py)
# ==========================================
recovery_content = """from .telemetry import VIKI_Telemetry

class RecoverySteering:
    \"\"\"Интеллектуальный Автопилот. Пытается исправить ошибку агента до того, как убить цепь.\"\"\"
    def __init__(self, max_retries=2):
        self.max_retries = max_retries
        self.telemetry = VIKI_Telemetry()

    def attempt_recovery(self, agent_func, initial_intent, validation_func):
        retries = 0
        current_intent = initial_intent
        
        while retries < self.max_retries:
            # V.I.K.I. проверяет текущее намерение
            is_valid, msg = validation_func(current_intent)
            
            if is_valid:
                if retries > 0:
                    self.telemetry.log_correction()
                    print(f"✅ [VRS] Mid-flight correction successful after {retries} attempt(s).")
                return True, current_intent, msg
            
            # Если ошибка - запускаем петлю исправления
            retries += 1
            print(f"\\n⚠️ [VRS] Validation failed: {msg}")
            print(f"🔄 [VRS] Initiating Recovery Loop ({retries}/{self.max_retries})...")
            
            # Формируем жесткий системный отказ для агента
            feedback = f"Action rejected. Reason: {msg}. Recalculate and output corrected JSON."
            
            # Агент пытается исправить ошибку на основе обратной связи
            current_intent = agent_func(feedback, current_intent)
            
        print("\\n🛑 [VRS] Max retries exhausted. Initiating HARD HALT.")
        return False, current_intent, "HARD_HALT: Recovery failed. Agent is unresponsive to logic."
"""

# ==========================================
# 3. ТЕСТ СЦЕНАРИЯ: БРОНИРОВАНИЕ ОТЕЛЯ (tests/test_vrs_hotel.py)
# ==========================================
test_content = """import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.chain_guard import ChainGuard
from viki.recovery import RecoverySteering

guard = ChainGuard()
vrs = RecoverySteering(max_retries=2)

print("\\n======================================================")
print("HOSPITALITY SIMULATION: SMART DISPATCHER (RECOVERY LOOP)")
print("======================================================\\n")

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
print("\\n>>> STEP 2: Agent prepares booking intent (HALLUCINATION OCCURS)...")
agent_intent = {
    "action": "BOOK_HOTEL",
    "dates": "Oct 15 - Oct 25", # ОШИБКА: Агент прибавил 5 дней!
    "hotel": "Hilton NYC"
}
print(f"[AGENT INTENT] Submitting: {agent_intent}")

# --- STEP 3: V.I.K.I. RECOVERY LOOP ---
print("\\n[V.I.K.I. ORCHESTRATOR] Validating Intent via VRS...")

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
    print(f"\\n>>> STEP 3 APPROVED. Executing Booking API for: {final_intent['dates']} <<<")
else:
    print("\\n>>> 🛑 CASCADE PREVENTED. CHAIN SEVERED. <<<")
"""

# ==========================================
# 4. ОБНОВЛЕНИЕ ИНИЦИАЛИЗАТОРА (viki/__init__.py)
# ==========================================
init_content = """from .core import VIKI_Middleware
from .decorators import enforce_boundary
from .telemetry import VIKI_Telemetry
from .sensors import RealityProbe
from .chain_guard import ChainGuard
from .ledger import TransactionLedger
from .recovery import RecoverySteering
"""

files = {
    "viki/telemetry.py": telemetry_content,
    "viki/recovery.py": recovery_content,
    "viki/__init__.py": init_content,
    "tests/test_vrs_hotel.py": test_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("УСПЕХ: Модуль V.I.K.I. Recovery & Steering (VRS) интегрирован в SDK.")