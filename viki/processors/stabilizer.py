import random
from typing import Dict, List

class AnchorEngine:
    """
    Stabilization Matrix v1.7.
    Strict co-regulation signals.
    """
    def __init__(self):
        self.anchors = {
            "emotional_high": [
                "I hear you. Going silent.",    # Слышу. Ухожу в тишину.
                "Understood. Remaining silent.", # Понял. Молчу.
                "Received. Going quiet."        # Принял. Замолкаю.
            ],
            "technical_high": [
                "Data fixed. Take a rest.",
                "Process paused. I am here."
            ],
            "general_high": [
                "I hear you. Moving to silence.",
                "Received. Going into silence."
            ]
        }

    def get_anchor(self, task_type: str) -> str:
        category = f"{task_type}_high"
        if category not in self.anchors: category = "general_high"
        return random.choice(self.anchors[category])