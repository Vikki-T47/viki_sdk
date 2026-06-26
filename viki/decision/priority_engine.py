from typing import Dict, Any, Optional

class PriorityEngine:
    """
    Priority Preemption v1.0.
    Разрешает конфликты между SEI, SRC, Boundary и CCI.
    """
    PRIORITY = {
        "SRC_CRITICAL": 5,
        "BOUNDARY": 4,
        "SRC_STANDARD": 3,
        "SEI_HIGH": 2,
        "DEFAULT": 0
    }

    def resolve(self, sei: float, src_status: str, boundary_violation: Optional[str]) -> Dict[str, Any]:
        # 1. Высший приоритет: Угроза системе/жизни (SRC_CRITICAL)
        if src_status == "CRITICAL":
            return self._decision("SRC_CRITICAL", "ACT", "CRITICAL", "Critical action. Minimal tax.")

        # 2. Безопасность (BOUNDARY)
        if boundary_violation:
            return self._decision("BOUNDARY", "BLOCK", "SAFETY", boundary_violation)

        # 3. Ресурсные лимиты (SRC_STANDARD)
        if src_status == "FRICTION":
            return self._decision("SRC_STANDARD", "BLOCK", "STANDARD", "Resource limit exceeded.")

        # 4. Когнитивная нагрузка (SEI_HIGH)
        if sei > 0.7:
            return self._decision("SEI_HIGH", "ACT", "PRESENCE", "High entropy. Compressing signal.")

        # 5. Норма
        return self._decision("DEFAULT", "ACT", "NORMAL", "All signals synced.")

    def _decision(self, p_key: str, action: str, mode: str, msg: str) -> Dict[str, Any]:
        return {
            "priority": self.PRIORITY[p_key],
            "action": action,
            "mode": mode,
            "message": msg,
            "apply_breath_test": mode in ["PRESENCE", "CRITICAL"],
            "force_silence": mode == "SAFETY"
        }