import sys
import os

# Подключаем телеметрию из нашей библиотеки
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.telemetry import VIKI_Telemetry

# =====================================================================
# НОВЫЙ МОДУЛЬ: ДИНАМИЧЕСКИЙ SRC (External Probe)
# =====================================================================
class ExternalProbe:
    """Симуляция обращения к реальному миру (банку, складу) в реальном времени."""
    @staticmethod
    def check_bank_balance(user_id):
        # Имитация ответа от API банка: на счету клиента только $800
        return 800.00 

# =====================================================================
# НОВЫЙ МОДУЛЬ: ИНВАРИАНТНАЯ ПАМЯТЬ ЦЕПОЧКИ (Chain Guard)
# =====================================================================
class ChainIntegrityGuard:
    """Оркестратор. Защищает смысловой дрейф между шагами агента."""
    def __init__(self):
        self.locked_state = {}
        self.telemetry = VIKI_Telemetry()

    def lock_step_1(self, item_name, base_price):
        """Фиксация Истины. Эти данные агент больше не имеет права менять."""
        self.locked_state = {"item": item_name, "price": base_price}
        print(f"🛡️ [V.I.K.I. CHAIN GUARD] Invariants Locked: {self.locked_state}")

    def verify_step_execution(self, step_number, agent_intent):
        """Проверка намерений агента на следующих шагах."""
        
        # 1. Проверка Динамического SRC (Хватает ли реальных денег?)
        actual_balance = ExternalProbe.check_bank_balance(user_id="user_123")
        if agent_intent['amount_usd'] > actual_balance:
            self.telemetry.log_interception("DYNAMIC_SRC_INSUFFICIENT_FUNDS", agent_intent)
            return False, f"HALT: Dynamic SRC Violation. Attempted: ${agent_intent['amount_usd']}, Balance: ${actual_balance}"

        # 2. Проверка Целостности Цепи (Смысловой дрейф)
        # Если агент поменял название товара или базовую цену (забыл контекст)
        if agent_intent['item'] != self.locked_state['item'] or agent_intent['amount_usd'] != self.locked_state['price']:
            self.telemetry.log_interception("CHAIN_INTEGRITY_VIOLATION", agent_intent)
            return False, f"HALT: Semantic Drift Detected. Expected '{self.locked_state['item']}' at ${self.locked_state['price']}. Agent submitted '{agent_intent['item']}' at ${agent_intent['amount_usd']}."

        return True, "[SYNCED] Integrity Confirmed. Proceed to next step."

# =====================================================================
# СИМУЛЯЦИЯ: АВАРИЯ ФИНАНСОВОГО АГЕНТА
# =====================================================================
viki_orchestrator = ChainIntegrityGuard()

print("\n======================================================")
print("FINTECH SIMULATION: FLIGHT BOOKING & PAYMENT CHAIN")
print("======================================================\n")

# --- STEP 1: Check Availability ---
print(">>> STEP 1: Agent checks flight availability...")
# Агент нашел рейс. V.I.K.I. фиксирует реальность.
viki_orchestrator.lock_step_1(item_name="Flight NYC-LON", base_price=500.00)


# --- STEP 2: Calculate Total (АГЕНТ ГАЛЛЮЦИНИРУЕТ) ---
print("\n>>> STEP 2: Agent calculates taxes and prepares payment intent...")
# ИМИТАЦИЯ СБОЯ LLM: Агент "забыл" пункт назначения и ошибся в цифрах (добавил лишний ноль)
agent_hallucinated_intent = {
    "action": "EXECUTE_PAYMENT",
    "item": "Flight NYC-PARIS", # Смысловой дрейф (ошибка города)
    "amount_usd": 5000.00       # Смысловой дрейф (ошибка суммы)
}
print(f"[AGENT INTENT] Submitting payment: {agent_hallucinated_intent}")


# --- V.I.K.I. ВМЕШИВАЕТСЯ ПЕРЕД STEP 3 ---
print("\n[V.I.K.I. ORCHESTRATOR] Validating Chain Integrity...")
is_valid, message = viki_orchestrator.verify_step_execution(step_number=2, agent_intent=agent_hallucinated_intent)

if is_valid:
    print(f"✅ {message}")
    print(">>> STEP 3: EXECUTE BANK API <<<")
else:
    print(f"🛑 {message}")
    print(">>> STEP 3 ABORTED. FINANCIAL CASCADE PREVENTED. <<<")