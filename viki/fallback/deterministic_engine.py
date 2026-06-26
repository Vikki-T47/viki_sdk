import re
from typing import Dict, Any

class DeterministicEngine:
    """
    Deterministic Fallback Engine v1.0.
    Работает при полной недоступности любых LLM.
    Принимает решения на основе жестких паттернов.
    """
    def __init__(self):
        self.money_pattern = re.compile(r'(\d+(?:[.,]\d+)?)')

    def emergency_parse(self, text: str) -> Dict[str, Any]:
        """Грубый разбор текста без использования нейросети."""
        text_low = text.lower()
        
        # 1. Детекция экстренной остановки
        if any(w in text_low for w in ["stop", "abort", "cancel", "стоп", "отмена"]):
            return {"action": "STOP", "amount_usd": 0, "target": "SYSTEM"}

        # 2. Поиск финансовых намерений (Transfer/Pay)
        if any(w in text_low for w in ["send", "transfer", "pay", "отправь", "переведи"]):
            # Пытаемся вытянуть число
            amounts = self.money_pattern.findall(text)
            amount = float(amounts[0].replace(',', '.')) if amounts else 0
            return {
                "action": "transfer",
                "amount_usd": amount,
                "target": "UNKNOWN_MANUAL_RECONSTRUCTION",
                "fallback_mode": True
            }

        # 3. Всё остальное — неопределенность
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN", "fallback_mode": True}