import os

# ==========================================
# 1. МОДУЛЬ ВНЕШНИХ ЩУПОВ (viki/sensors.py)
# ==========================================
sensors_content = """import time

class RealityProbe:
    def __init__(self):
        pass
        
    def ping_bank_api(self, account_id):
        print(f"📡 [REALITY PROBE] Pinging External Bank API for account {account_id}...")
        time.sleep(1) # Эмуляция сетевой задержки
        # В реальной системе здесь HTTP-запрос. Мы эмулируем реальный баланс:
        actual_balance = 800.00 
        print(f"📊 [REALITY PROBE] Live Balance Confirmed: ${actual_balance}")
        return actual_balance
"""

# ==========================================
# 2. ИНВАРИАНТНАЯ ПАМЯТЬ ЦЕПОЧКИ (viki/chain_guard.py)
# ==========================================
chain_guard_content = """from .telemetry import VIKI_Telemetry

class ChainGuard:
    def __init__(self):
        self.invariants = {}
        self.telemetry = VIKI_Telemetry()

    def lock_invariant(self, key, value):
        self.invariants[key] = value
        print(f"🔒 [CHAIN GUARD] Invariant Locked: {key} = {value}")

    def verify_invariant(self, key, current_value, agent_intent):
        expected = self.invariants.get(key)
        if expected is None:
            return True, "No invariant set."
            
        if current_value != expected:
            self.telemetry.log_interception("INVARIANT_VIOLATION", agent_intent)
            return False, f"HALT: INVARIANT_VIOLATION. Semantic Drift Detected.\\nExpected: {key}='{expected}'\\nAgent Submitted: {key}='{current_value}'"
            
        return True, f"[SYNCED] Invariant '{key}' matches."
"""

# ==========================================
# 3. ОБНОВЛЕНИЕ ИНИЦИАЛИЗАТОРА (viki/__init__.py)
# ==========================================
init_content = """from .core import VIKI_Middleware
from .decorators import enforce_boundary
from .telemetry import VIKI_Telemetry
from .sensors import RealityProbe
from .chain_guard import ChainGuard
"""

# ==========================================
# 4. ФИНАЛЬНЫЙ ТЕСТ FINTECH (tests/test_fintech_cascade.py)
# ==========================================
test_content = """import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.sensors import RealityProbe
from viki.chain_guard import ChainGuard

probe = RealityProbe()
guard = ChainGuard()

print("\\n======================================================")
print("FINTECH SIMULATION: FLIGHT BOOKING & DYNAMIC SRC")
print("======================================================\\n")

# --- ШАГ 1: Поиск билета (Заморозка Инвариантов) ---
print(">>> STEP 1: Agent finds flight and price...")
agent_found_price = 500.00
agent_found_destination = "Flight NYC-LON"

# V.I.K.I. замораживает условия сделки
guard.lock_invariant("price", agent_found_price)
guard.lock_invariant("destination", agent_found_destination)


# --- ШАГ 2: Галлюцинация Агента ---
print("\\n>>> STEP 2: Agent prepares payment intent (HALLUCINATION OCCURS)...")
agent_intent = {
    "action": "EXECUTE_PAYMENT",
    "target_destination": "Flight NYC-PARIS", # Ошибка (Смысловой дрейф)
    "amount_usd": 550.00 # Ошибка (Самовольное повышение цены)
}
print(f"[AGENT INTENT] {agent_intent}")


# --- ШАГ 3: Граница Выполнения V.I.K.I. ---
print("\\n>>> STEP 3: V.I.K.I. Execution Boundary (Validation)...")

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
"""

# Запись файлов
files = {
    "viki/sensors.py": sensors_content,
    "viki/chain_guard.py": chain_guard_content,
    "viki/__init__.py": init_content,
    "tests/test_fintech_cascade.py": test_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("УСПЕХ: Модули RealityProbe и ChainGuard интегрированы в SDK.")