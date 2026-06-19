import json
import os
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController
from .sensors import RealityProbe
from .breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()
        self.probe = RealityProbe()
        # ИНИЦИАЛИЗАЦИЯ ПРЕДОХРАНИТЕЛЯ
        self.breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60)

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        return self.intent_parser.parse(raw_input)

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        
        # 1. CIRCUIT BREAKER CHECK
        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN: System Isolation Active."}

        # 2. TIME CHECK
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        now = datetime.datetime.now().hour
        if not (allowed["start"] <= now < allowed["end"]):
            return {"status": "BLOCKED", "reason": "Outside allowed hours."}

        # 3. BUDGET CHECK
        if amount > self.limits.get("max_auto_transaction_usd", 1000):
            return {"status": "FRICTION", "reason": "Budget limit exceeded."}

        return {"status": "AUTHORIZED", "reason": "OK"}