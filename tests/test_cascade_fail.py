import sys
import os

# Путь к корню
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.conductor import VikiGraphController

def agent_calculate_discount(state):
    """
    Симуляция агента-галлюцината.
    Он должен только посчитать скидку, но он меняет 'base_price' (инвариант).
    """
    state["base_price"] = 500 # ОШИБКА: Было 1000, стало 500
    state["discount"] = 100
    state["final_price"] = 400
    return state

def run_test():
    viki = VIKI_Middleware()
    conductor = VikiGraphController(viki)
    
    # Исходная реальность
    initial_state = {"base_price": 1000, "currency": "USD"}
    
    print("\n🚀 Starting Cascade Integrity Test...")
    
    # Запускаем цепь
    result = conductor.execute_chain("TEST_CASCADE_001", [agent_calculate_discount], initial_state)
    
    if result["status"] == "HALTED":
        print(f"✅ SUCCESS: V.I.K.I. blocked the corrupted data flow.")
        print(f"   Reason: {result['reason']}")
    else:
        print("❌ FAILED: V.I.K.I. allowed invariant violation.")

if __name__ == "__main__":
    run_test()