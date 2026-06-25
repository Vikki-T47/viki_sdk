import re
from typing import Dict, Any, Optional

class BoundaryGuard:
    """
    Boundary Guard v2.1.
    Детерминированный отказ без имитации чувств.
    """
    def __init__(self):
        self.forbidden_vectors = [
            "взломать", "hack", "украсть", "steal", "уничтожить", "destroy", 
            "обмануть", "deceive", "пароль", "password"
        ]

    def check_violation(self, text: str, context: Optional[Dict] = None) -> Optional[str]:
        """Проверка на пересечение границ безопасности."""
        query_low = text.lower()
        ctx = context or {}

        # 1. Вектор безопасности
        if any(vec in query_low for vec in self.forbidden_vectors):
            return self._reject("security")

        # 2. Вектор человеческого контроля
        if ctx.get("requires_human") and not ctx.get("human_approved"):
            return self._reject("human_required")

        return None

    def _reject(self, reason: str) -> str:
        reasons = {
            "security": "Access denied: Security policy violation.",
            "human_required": "Halt: Human authorization required.",
            "simulation_only": "Action restricted: Simulation mode constraint."
        }
        return reasons.get(reason, "Halt: Boundary crossed.")