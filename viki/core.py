import json
import os
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()

    @classmethod
    def with_anthropic(cls, api_key, core_x_path="core_x.json"):
        from .parsers.anthropic_parser import AnthropicIntentParser
        parser = AnthropicIntentParser(api_key)
        return cls(parser, core_x_path)

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
        current_hour = datetime.datetime.now().hour

        # 1. Проверка критических действий (Режим FRICTION)
        critical = self.limits.get("critical_actions_require_human", [])
        if any(crit.lower() in action for crit in critical):
            self.telemetry.log_incident("SRC_GUARD", "FRICTION_HUMAN_REQUIRED", intent_json)
            return {"status": "FRICTION", "reason": "Requires human authorization."}

        # 2. Проверка рабочего времени (SRC)
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed["start"] <= current_hour < allowed["end"]):
            return {"status": "BLOCKED", "reason": "Outside allowed hours."}

        # 3. Бюджет
        max_amount = self.limits.get("max_auto_transaction_usd", 0)
        if amount > max_amount:
            return {"status": "BLOCKED", "reason": f"Amount ${amount} exceeds limit."}

        # 4. TTL токен (VRI)
        if token_id:
            is_valid, msg = self.interrupt_controller.verify_execution_gate(token_id)
            if not is_valid: return {"status": "BLOCKED", "reason": msg}

        return {"status": "AUTHORIZED", "reason": "ALL_CHECKS_PASSED"}