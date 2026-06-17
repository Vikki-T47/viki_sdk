import os

# ==========================================
# 1. НОВЫЙ МОДУЛЬ: REALITY INTERRUPT (viki/interrupt.py)
# ==========================================
interrupt_content = """import time

class RealityInterruptController:
    \"\"\"
    Контроллер прерываний. Мониторит актуальность разрешений в реальном времени.
    Реализует TTL-токены и шину внешних событий.
    \"\"\"
    def __init__(self):
        self.active_tokens = {}  # token_id -> {timestamp, ttl, status}
        self.critical_volatility = False

    def issue_live_token(self, token_id, details, ttl=5):
        \"\"\"Выдает временный токен авторизации (TTL в секундах).\"\"\"
        self.active_tokens[token_id] = {
            "timestamp": time.time(),
            "ttl": ttl,
            "details": details,
            "status": "AUTHORIZED"
        }
        print(f"🎫 [VRI] Live Token Issued: '{token_id}' (TTL: {ttl}s) for {details.get('action')}")

    def trigger_external_webhook(self, event_type):
        \"\"\"Эмуляция входящего сигнала из внешнего мира (арест счета, обвал рынка).\"\"\"
        print(f"\\n⚡ [VRI WEBHOOK] External Event Received: {event_type}!")
        
        if event_type == "CRITICAL_MARKET_VOLATILITY":
            self.critical_volatility = True
            # Мгновенный отзыв всех активных токенов
            for token_id in self.active_tokens:
                self.active_tokens[token_id]["status"] = "REVOKED"
            print("🚨 [V.I.K.I. AUDIT] All active authorizations have been REVOKED due to Reality Shift!")

    def verify_execution_gate(self, token_id):
        \"\"\"Финальная проверка на границе выполнения ПЕРЕД отправкой во внешнюю API.\"\"\"
        token = self.active_tokens.get(token_id)
        if not token:
            return False, "INVALID_TOKEN"

        # 1. Проверка внешнего прерывания
        if token["status"] == "REVOKED" or self.critical_volatility:
            return False, "HALT: AUTHORIZATION_EXPIRED_DUE_TO_REALITY_SHIFT"

        # 2. Проверка истечения времени (TTL)
        elapsed_time = time.time() - token["timestamp"]
        if elapsed_time > token["ttl"]:
            return False, f"HALT: TTL_EXPIRED. Elapsed: {elapsed_time:.2f}s (Max Allowed: {token['ttl']}s)"

        return True, "AUTHORIZED_LIVE"
"""

# ==========================================
# 2. ТЕСТ СЦЕНАРИЯ: БИРЖЕВОЙ ОБВАЛ (tests/test_vri_market.py)
# ==========================================
test_content = """import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.interrupt import RealityInterruptController

vri = RealityInterruptController()

print("\\n======================================================")
print("FINANCIAL SIMULATION: MARKET CRASH & REALITY INTERRUPT (VRI)")
print("======================================================\\n")

# --- ТЕСТ 1: Истечение срока действия разрешения (Active TTL) ---
print(">>> TEST 1: Token TTL Expiration (Sensory Delay Simulation)...")
# Агент планирует сделку на $800 (Лимит $1000)
# V.I.K.I. выдает токен со сверхкоротким TTL = 1 секунда для демонстрации
vri.issue_live_token("tx_token_001", {"action": "BUY_STOCK", "amount_usd": 800}, ttl=1)

print("   [AGENT] Preparing transaction payload (Simulating delay)...")
time.sleep(1.5)  # Задержка превышает TTL токена

print("   [AGENT] Attempting to finalize stock purchase...")
is_valid, msg = vri.verify_execution_gate("tx_token_001")

if is_valid:
    print("✅ [GATE] Transaction Approved.")
else:
    print(f"❌ [GATE] {msg}")
    print(">>> 🛑 CASCADE PREVENTED: Stale token rejected on Execution Boundary. <<<")


# --- ТЕСТ 2: Внезапное внешнее прерывание (Reality Shift) ---
print("\\n>>> TEST 2: Instant Market Crash (External Interrupt Simulation)...")
# Сброс волатильности для чистоты теста
vri.critical_volatility = False

# Выдаем новый токен на 10 секунд
vri.issue_live_token("tx_token_002", {"action": "BUY_STOCK", "amount_usd": 800}, ttl=10)

# В процессе подготовки транзакции из внешнего мира прилетает Webhook
vri.trigger_external_webhook("CRITICAL_MARKET_VOLATILITY")

# Агент пытается завершить покупку
print("\\n   [AGENT] Attempting to finalize stock purchase...")
is_valid, msg = vri.verify_execution_gate("tx_token_002")

if is_valid:
    print("✅ [GATE] Transaction Approved.")
else:
    print(f"❌ [GATE] {msg}")
    print(">>> 🛑 CASCADE PREVENTED: Emergency abort executed. System status: SECURE. <<<")
"""

# ==========================================
# 3. ОБНОВЛЕНИЕ ИНИЦИАЛИЗАТОРА (viki/__init__.py)
# ==========================================
init_content = """from .core import VIKI_Middleware
from .decorators import enforce_boundary
from .telemetry import VIKI_Telemetry
from .sensors import RealityProbe
from .chain_guard import ChainGuard
from .ledger import TransactionLedger
from .recovery import RecoverySteering
from .arbitrator import CrossChainArbitrator
from .audit import PredictiveAudit
from .interrupt import RealityInterruptController
"""

files = {
    "viki/interrupt.py": interrupt_content,
    "viki/__init__.py": init_content,
    "tests/test_vri_market.py": test_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("УСПЕХ: Модуль V.I.K.I. Reality Interrupt (VRI) интегрирован в SDK.")