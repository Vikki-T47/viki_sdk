import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.ledger import TransactionLedger
from viki.arbitrator import CrossChainArbitrator

flight_ledger = TransactionLedger("Flight_Agent")
hotel_ledger = TransactionLedger("Hotel_Agent")
arbitrator = CrossChainArbitrator()

print("\n======================================================")
print("MULTI-AGENT SIMULATION: COMPLEX TRAVEL (CROSS-CHAIN ARBITRATION)")
print("======================================================\n")

# Регистрация Мета-задачи
arbitrator.register_meta_task(meta_task_id="TRIP_NYC_001", ledgers=[flight_ledger, hotel_ledger])

# --- ПАРАЛЛЕЛЬНЫЙ ПРОЦЕСС 1: FLIGHT AGENT ---
print("\n>>> PROCESS 1: Flight Agent executing...")
print("   [API] Booking Flight to NYC...")
# Агент успешно забронировал рейс
flight_ledger.commit_step(
    step_id="BOOK_FLIGHT", 
    details={"route": "LHR-JFK", "price": 400}, 
    rollback_instruction={"api": "/flight/cancel", "id": "FL-9982"}
)

# --- ПАРАЛЛЕЛЬНЫЙ ПРОЦЕСС 2: HOTEL AGENT (АВАРИЯ) ---
print("\n>>> PROCESS 2: Hotel Agent executing...")
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

print("\n>>> META-TASK ABORTED. SYSTEM STATE RESTORED. <<<\n")
