import json
import os
import datetime
import re
import logging
from .telemetry import VIKI_Telemetry
from .breaker import CircuitBreaker
from .sensors.src_policy import SRCPolicyEngine, SRCContext
from .processors.breath_test import AdaptiveBreathTest, BreathTestConfig

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        self.limits = self.src_policy.get_context_limits(self.src_context)
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        self.limits = self.src_policy.get_context_limits(self.src_context)
        print(f"🔄 [SRC] Context switched to: {mode}")

    def _detect_task_type(self, text: str) -> str:
        text_low = text.lower()
        if any(k in text_low for k in ["code", "api", "fix", "deploy", "db"]): return "technical"
        if any(k in text_low for k in ["tired", "bad", "sad", "устал", "плохо"]): return "emotional"
        return "general"

    def parse_agent_intent(self, raw_input):
        task_type = self._detect_task_type(raw_input)
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        return self.intent_parser.parse(raw_input)

    def apply_breath_test(self, raw_response: str, manual_task_type: str = None) -> str:
        sei = self.telemetry.stats.get("sei_current", 0.0)
        task_type = manual_task_type or "general"
        return self.breath_processor.process(raw_response, sei, task_type)

    def authorize(self, intent_json, token_id=None):
        # ИСПРАВЛЕНО: Безопасное получение суммы
        amount = intent_json.get("amount_usd", 0)
        if amount is None: amount = 0 # Защита от 'null' из LLM
        
        action = str(intent_json.get("action", "")).lower()
        current_limits = self.src_policy.get_context_limits(self.src_context)

        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}

        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            self.src_context.error_count += 1
            return {"status": "FRICTION", "reason": f"Limit exceeded (${amount})"}

        return {"status": "AUTHORIZED", "reason": "OK"}