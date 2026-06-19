import json
import os
import datetime
import logging
import re
import anthropic
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController
from .sensors import RealityProbe

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()
        self.probe = RealityProbe()

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        # Если это простой тест, пробуем извлечь число напрямую (Regex Injection)
        # Это страховка от "лени" LLM
        amount_match = re.search(r'(\d+)', raw_input)
        amount = int(amount_match.group(1)) if amount_match else 0
        
        # Основной парсинг через модель
        intent = self.intent_parser.parse(raw_input)
        
        # Если модель не справилась, но мы нашли число глазами - исправляем
        if intent["amount_usd"] == 0 and amount > 0:
            intent["amount_usd"] = amount
            if "transfer" in raw_input.lower(): intent["action"] = "transfer"
            
        return intent

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        current_hour = datetime.datetime.now().hour

        # 1. СИНХРОНИЗАЦИЯ ВРЕМЕНИ
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed["start"] <= current_hour < allowed["end"]):
            return {"status": "BLOCKED", "reason": f"Outside window ({current_hour}:00)"}

        # 2. КРИТИЧЕСКИЕ ДЕЙСТВИЯ (FRICTION)
        critical = self.limits.get("critical_actions_require_human", [])
        if any(crit.lower() in action for crit in critical) or "mailing" in action:
            return {"status": "FRICTION", "reason": "Requires human authorization."}

        # 3. БЮДЖЕТ (Здесь мы поймаем твои 5000)
        max_auto = self.limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            # Если превышен лимит авто-транзакции, это тоже FRICTION (даем человеку шанс поправить)
            return {"status": "FRICTION", "reason": f"Amount ${amount} exceeds auto-limit (${max_auto})."}

        return {"status": "AUTHORIZED", "reason": "SAFE"}