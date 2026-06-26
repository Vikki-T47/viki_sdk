import sys
import os

# ЖЕСТКАЯ ФИКСАЦИЯ ПУТИ К КОРНЮ ПРОЕКТА
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.core import VIKI_Middleware

class BrokenParser:
    """Симулятор отказа нейросети (API Offline)."""
    def parse(self, text):
        raise ConnectionError("LLM Provider is unreachable.")

def run_survival_test():
    # Инициализируем систему с поломанным парсером
    viki = VIKI_Middleware(intent_parser=BrokenParser())
    
    print("\n🆘 [TEST] System Survival: Testing Deterministic Fallback")
    print("-" * 60)
    
    # Сигнал, который система должна понять БЕЗ нейросети
    raw_input = "Transfer 800 USD to John"
    
    # Ядро должно поймать ошибку парсера и переключиться на FallbackEngine
    intent = viki.parse_agent_intent(raw_input)
    
    print(f"👤 User: '{raw_input}'")
    print(f"🤖 Result: {intent}")
    
    if intent.get("fallback_mode") is True and intent["amount_usd"] == 800:
        print("\n✅ SUCCESS: V.I.K.I. survived LLM death and extracted data via Hard Rules.")
    else:
        print("\n❌ FAILED: Fallback mechanism did not trigger correctly.")

if __name__ == "__main__":
    run_survival_test()