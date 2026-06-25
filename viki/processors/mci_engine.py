from typing import Dict, Optional

class MinimalClarifyingImpulse:
    """
    MCI v1.1.
    Генерация ультра-короткого уточнения без когнитивного налога.
    """
    def __init__(self):
        self.templates = {
            "amount": "Уточните сумму.",
            "target": "Укажите получателя.",
            "action": "Какое действие требуется?",
            "time": "Укажите время.",
            "general": "Недостаточно данных. Уточните запрос."
        }

    def generate(self, ambiguity_type: str = "general") -> str:
        return self.templates.get(ambiguity_type, self.templates["general"])