import json
import os
import datetime
import logging
import re
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController
from .breaker import CircuitBreaker
from .parsers.anthropic_parser import AnthropicIntentParser
from .parsers.local_parser import LocalIntentParser

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        
        # АВТО-ВЫБОР ПРОВАЙДЕРА (v1.7.2)
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            provider = self.limits.get("provider", "local").lower()
            if provider == "local":
                local_cfg = self.limits.get("local_config", {})
                self.intent_parser = LocalIntentParser(
                    base_url=local_cfg.get("base_url", "http://localhost:11434/v1"),
                    model=local_cfg.get("model", "llama3")
                )
            else:
                api_key = os.getenv("ANTHROPIC_API_KEY", "STABLE_TEST")
                self.intent_parser = AnthropicIntentParser(api_key=api_key)

        self.interrupt_controller = RealityInterruptController()
        self.breaker = CircuitBreaker()

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        self.telemetry.calculate_sei(raw_input)
        return self.intent_parser.parse(raw_input)

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        
        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}
            
        max_auto = self.limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            return {"status": "FRICTION", "reason": f"Amount ${amount} exceeds limit."}
            
        return {"status": "AUTHORIZED", "reason": "OK"}