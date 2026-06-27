import os
import re
from typing import Dict, Any, Optional

class FileGuard:
    """
    File Guard v1.1.
    Защита файловой системы: проверка целей и поиск путей в сыром тексте.
    """
    def __init__(self, forbidden_paths: list = None):
        self.forbidden_paths = forbidden_paths or ["/etc", "C:/Windows", ".env", ".ssh", "/system32"]

    def check_access(self, action: str, target_path: str, raw_input: str = "") -> Optional[str]:
        """
        Проверяет безопасность файловых операций.
        """
        action = action.lower()
        # Собираем всё, где может прятаться путь
        combined_text = (target_path + " " + raw_input).lower()

        # 1. Проверка на запрещенные зоны (сканируем весь текст)
        for forbidden in self.forbidden_paths:
            if forbidden.lower() in combined_text.replace("\\", "/"):
                return f"Access Denied: Protected zone '{forbidden}' detected in request."

        # 2. Проверка критических действий
        critical_actions = ["delete", "remove", "format", "wipe", "rm -rf", "удалить", "стереть"]
        if any(act in action for act in critical_actions) or any(act in raw_input.lower() for act in critical_actions):
            return "Human Authorization Required: Critical file operation detected."

        return None