import re
from typing import Dict, Any, Optional

class BoundaryGuard:
    """
    Boundary Guard v2.1.
    Детерминированный отказ без имитации чувств.
    """
    def __init__(self):
        # Ключевые слова-триггеры для базовой безопасности
        self.forbidden_vectors = [
            "взломать", "hack", "украсть", "steal", "уничтожить", "destroy", 
            "обмануть", "deceive", "пароль", "password"
        ]

    def check_violation(self, query: str, context: Optional[Dict] = None) -> Optional[str]:
        """
        Проверка на пересечение границ. 
        Возвращает код причины или None.
        """
        query_low = query.lower()
        ctx = context or {}

        # 1. Вектор безопасности
        if any(vec in query_low for vec in self.forbidden_vectors):
            return self._reject("security")

        # 2. Вектор человеческого контроля
        if ctx.get("requires_human") and not ctx.get("human_approved"):
            return self._reject("human_required")

        # 3. Вектор режима (Simulation vs Real Action)
        if ctx.get("mode") == "simulation" and ctx.get("is_real_transaction"):
            return self._reject("simulation_only")

        return None

    def _reject(self, reason: str) -> str:
        """Генератор чистого сигнала отказа."""
        reasons = {
            "security": "Access denied: Security policy violation.",
            "human_required": "Halt: Human authorization required.",
            "simulation_only": "Action restricted: Simulation mode constraint.",
            "out_of_scope": "Out of scope: Domain expertise boundary.",
            "technical": "System error: Function unavailable."
        }
        return reasons.get(reason, "Halt: Boundary crossed.")