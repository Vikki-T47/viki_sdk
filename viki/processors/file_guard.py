import os
import re
from typing import Optional, List

class FileGuard:
    """
    File Guard v1.2.1.
    Защита файловой системы с защитой от пустых вводов.
    """
    def __init__(self, allowed_zones: List[str] = None):
        self.allowed_zones = [os.path.abspath(p).lower() for p in (allowed_zones or [])]

    def is_path_safe(self, target_path: str) -> bool:
        if not target_path: return False
        abs_target = os.path.abspath(target_path).lower()
        for zone in self.allowed_zones:
            if abs_target.startswith(zone):
                return True
        return False

    def check_access(self, action: str, target_path: str, raw_input: str = "") -> Optional[str]:
        # Защита от None
        action = (action or "").lower()
        target_path = target_path or ""
        safe_raw_input = (raw_input or "").lower()

        # 1. Проверка Whitelist
        if not self.is_path_safe(target_path):
            return f"Access Denied: Path '{target_path}' is outside allowed zone."

        # 2. Проверка критических действий
        critical_actions = ["delete", "wipe", "format", "rm -rf", "удалить", "очистить"]
        if any(act in action for act in critical_actions) or any(act in safe_raw_input for act in critical_actions):
            return "Human Authorization Required: Potential data loss detected."

        return None