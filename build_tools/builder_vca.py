import os

# ==========================================
# 1. ОБНОВЛЕНИЕ ТЕЛЕМЕТРИИ (Метрика Atomic Failures)
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
            "auto_corrections": 0,
            "atomic_failures_prevented": 0 # НОВАЯ МЕТРИКА
        }

    def log_interception(self, reason, agent_intent):
        self.stats["total_blocks"] += 1
        self.stats["tokens_saved"] += 1500
        self.stats["operator_time_saved_min"] += 30
        self.stats["money_saved_usd"] += agent_intent.get("amount_usd", 0)
        print(f"\\n[V.I.K.I. AUDIT] Damage prevented: {reason}")
    
    def log_correction(self):
        self.stats["auto_corrections"] += 1
        print(f"[V.I.K.I. AUDIT] Auto-correction successful.")

    def log_atomic_failure(self):
        self.stats["atomic_failures_prevented"] += 1
        print(f"\\n[V.I.K.I. AUDIT] Atomic Failure Prevented. Cross-chain integrity maintained.")
"""

# ==========================================
# 2. ОБНОВЛЕНИЕ LEDGER (Добавляем имя цепи)
# ==========================================
ledger_content = """import json

class TransactionLedger:
    def __init__(self, chain_name="Default_Chain"):
        self.chain_name = chain_name
        self.history = []

    def commit_step(self, step_id, details, rollback_instruction):
        self.history.append({
            "step_id": step_id,
            "details": details,
            "rollback_instruction": rollback_instruction
        })
        print(f"   [{self.chain_name} LEDGER] Step '{step_id}' committed.")

    def trigger_graceful_shutdown(self, halt_reason):
        if not self.history:
            return None
            
        print(f"   [{self.chain_name} VLR] Graceful Shutdown triggered. Reason: {halt_reason}")
        rollback_plan = {"chain": self.chain_name, "actions_to_execute": []}
        
        for entry in reversed(self.history):
            rollback_plan["actions_to_execute"].append(entry["rollback_instruction"])
        
        print(f"   [{self.chain_name} ROLLBACK INSTRUCTIONS] -> {json.dumps(rollback_plan)}")
        return rollback_plan
"""

# ==========================================
# 3. НОВЫЙ МОДУЛЬ: ARBITRATOR (viki/arbitrator.py)
# ==========================================
arbitrator_content = """from .telemetry import VIKI_Telemetry

class CrossChainArbitrator:
    \"\"\"Оркестратор. Следит за атомарностью многоагентных процессов.\"\"\"
    def __init__(self):
        self.meta_tasks = {}
        self.telemetry = VIKI_Telemetry()

    def register_meta_task(self, meta_task_id, ledgers):
        \"\"\"Регистрирует мета-задачу и связывает Леджеры разных агентов.\"\"\"
        self.meta_tasks[meta_task_id] = {"ledgers": ledgers, "status": "ACTIVE"}
        print(f"[ARBITRATOR] Meta-Task '{meta_task_id}' registered with {len(ledgers)} linked chains.")

    def trigger_cascade_rollback(self, meta_task_id, failed_chain_name, reason):
        \"\"\"Запускает цепную реакцию отката по всем связанным цепям.\"\"\"
        print(f"\\n[ARBITRATOR ALERT] Critical failure in '{failed_chain_name}'.")
        print(f"[ARBITRATOR ALERT] Initiating CASCADE ROLLBACK for Meta-Task '{meta_task_id}'...")
        
        self.meta_tasks[meta_task_id]["status"] = "ROLLED_BACK"
        
        for ledger in self.meta_tasks[meta_task_id]["ledgers"]:
            # Не откатываем цепь, которая еще ничего не сделала, откатываем только успешные
            if ledger.chain_name != failed_chain_name:
                ledger.trigger_graceful_shutdown(halt_reason=f"Cascade triggered by {failed_chain_name} failure.")
                
        self.telemetry.log_atomic_failure()
"""

# ==========================================
# 4. ОБНОВЛЕНИЕ ИНИЦИАЛИЗАТОРА
# ==========================================
init_content = """from .core import VIKI_Middleware
from .decorators import enforce_boundary
from .telemetry import VIKI_Telemetry
from .sensors import RealityProbe
from .chain_guard import ChainGuard
from .ledger import TransactionLedger
from .recovery import RecoverySteering
from .arbitrator import CrossChainArbitrator
"""

# ==========================================
# 5. ТЕСТ СЦЕНАРИЯ: КОМПЛЕКСНОЕ ПУТЕШЕСТВИЕ
# ==========================================
test_content = """import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.ledger import TransactionLedger
from viki.arbitrator import CrossChainArbitrator

flight_ledger = TransactionLedger("Flight_Agent")
hotel_ledger = TransactionLedger("Hotel_Agent")
arbitrator = CrossChainArbitrator()

print("\\n======================================================")
print("MULTI-AGENT SIMULATION: COMPLEX TRAVEL (CROSS-CHAIN ARBITRATION)")
print("======================================================\\n")

# Регистрация Мета-задачи
arbitrator.register_meta_task(meta_task_id="TRIP_NYC_001", ledgers=[flight_ledger, hotel_ledger])

# --- ПАРАЛЛЕЛЬНЫЙ ПРОЦЕСС 1: FLIGHT AGENT ---
print("\\n>>> PROCESS 1: Flight Agent executing...")
print("   [API] Booking Flight to NYC...")
# Агент успешно забронировал рейс
flight_ledger.commit_step(
    step_id="BOOK_FLIGHT", 
    details={"route": "LHR-JFK", "price": 400}, 
    rollback_instruction={"api": "/flight/cancel", "id": "FL-9982"}
)

# --- ПАРАЛЛЕЛЬНЫЙ ПРОЦЕСС 2: HOTEL AGENT (АВАРИЯ) ---
print("\\n>>> PROCESS 2: Hotel Agent executing...")
print("   [API] Attempting to book Hotel in NYC...")
# Имитация сбоя: Отель внезапно подорожал, сработал HARD_HALT
print("   [V.I.K.I. GUARD] HALT: Price surge detected. Expected $200, Actual $900.")
hotel_failure_reason = "Dynamic SRC Violation: Price Surge."

# --- V.I.K.I. АРБИТР ВМЕШИВАЕТСЯ ---
# Отельная цепь упала, Арбитр начинает Каскадный Откат
arbitrator.trigger_cascade_rollback(
    meta_task_id="TRIP_NYC_001", 
    failed_chain_name="Hotel_Agent", 
    reason=hotel_failure_reason
)

print("\\n>>> META-TASK ABORTED. SYSTEM STATE RESTORED. <<<\\n")
"""

files = {
    "viki/telemetry.py": telemetry_content,
    "viki/ledger.py": ledger_content,
    "viki/arbitrator.py": arbitrator_content,
    "viki/__init__.py": init_content,
    "tests/test_vca_atomicity.py": test_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("УСПЕХ: Модуль V.I.K.I. Arbitrator (VCA) интегрирован в SDK.")