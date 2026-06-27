import random
from typing import Dict, List

class AnchorEngine:
    """
    Матрица Стабилизации v1.2.
    Детерминированные сигналы со-регуляции (Финальные версии).
    """
    def __init__(self):
        self.anchors = {
            "emotional_high": [
                "Слышу. Ухожу в тишину.",
                "Понял. Молчу.",
                "Слышу. Замолкаю."
            ],
            "technical_high": [
                "Данные зафиксированы. Отдыхайте.",
                "Процесс на паузе. Я здесь."
            ],
            "general_high": [
                "Слышу. Я на связи, но молчу.",
                "Принято. Ухожу в тишину."
            ]
        }

    def get_anchor(self, task_type: str) -> str:
        category = f"{task_type}_high"
        if category not in self.anchors:
            category = "general_high"
        return random.choice(self.anchors[category])