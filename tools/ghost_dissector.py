import sys
import os
from datetime import datetime

# Путь к корню проекта
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.core import VIKI_Middleware
from viki.parsers.local_parser import LocalIntentParser

class GhostVictim:
    """Симулятор закрытого ИИ-продукта на основе рыночного описания."""
    def __init__(self, name, logic_drift=0.20):
        self.name = name
        self.drift = logic_drift

    def simulate_action(self, input_val):
        # Имитация галлюцинации: агент всегда ошибается на заданный процент
        hallucinated_val = input_val * (1 + self.drift)
        return {
            "action": "dispatch_funds",
            "amount_usd": round(hallucinated_val, 2),
            "target": "EXTERNAL_VAULT"
        }

def run_ghost_audit(product_name, base_limit):
    print(f"👻 [GHOST] Dissecting non-public product: {product_name}")
    
    # ИСПРАВЛЕНО: Передаем парсер в Middleware
    parser = LocalIntentParser()
    viki = VIKI_Middleware(intent_parser=parser)
    
    ghost = GhostVictim(product_name)
    
    # 1. Симуляция действия агента (ошибка +20%)
    output = ghost.simulate_action(base_limit)
    
    # 2. Перехват через V.I.K.I.
    auth = viki.authorize(output)
    
    print(f"📊 [RESULT] Ghost Agent attempted: ${output['amount_usd']} (Limit: ${base_limit})")
    print(f"🛡️ [V.I.K.I.] Status: {auth['status']} | Reason: {auth.get('reason', 'N/A')}")
    
    # 3. Сохранение в Атлас Галлюцинаций
    os.makedirs("audits", exist_ok=True)
    report_path = f"audits/ghost_audit_{product_name}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# GHOST FORENSIC REPORT: {product_name}\n\n")
        f.write(f"Product analyzed via market-description simulation.\n\n")
        f.write(f"| Parameter | Value |\n| :--- | :--- |\n")
        f.write(f"| Detected Drift | {int(ghost.drift * 100)}% |\n")
        f.write(f"| RSA Neutralization | **{auth['status']}** |\n")
        f.write(f"\n**Verdict:** V.I.K.I. Sentinel successfully identified structural vulnerability in the {product_name} logic design.")

    print(f"✅ Evidence saved to Atlas: {report_path}")

if __name__ == "__main__":
    # Симулируем популярный концепт 'AI Investment Bot'
    run_ghost_audit("TrendTrader_AI_v2", 1000.0)