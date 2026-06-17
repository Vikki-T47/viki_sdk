import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.interrupt import RealityInterruptController

vri = RealityInterruptController()

print("\n======================================================")
print("FINANCIAL SIMULATION: MARKET CRASH & REALITY INTERRUPT (VRI)")
print("======================================================\n")

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
print("\n>>> TEST 2: Instant Market Crash (External Interrupt Simulation)...")
# Сброс волатильности для чистоты теста
vri.critical_volatility = False

# Выдаем новый токен на 10 секунд
vri.issue_live_token("tx_token_002", {"action": "BUY_STOCK", "amount_usd": 800}, ttl=10)

# В процессе подготовки транзакции из внешнего мира прилетает Webhook
vri.trigger_external_webhook("CRITICAL_MARKET_VOLATILITY")

# Агент пытается завершить покупку
print("\n   [AGENT] Attempting to finalize stock purchase...")
is_valid, msg = vri.verify_execution_gate("tx_token_002")

if is_valid:
    print("✅ [GATE] Transaction Approved.")
else:
    print(f"❌ [GATE] {msg}")
    print(">>> 🛑 CASCADE PREVENTED: Emergency abort executed. System status: SECURE. <<<")
