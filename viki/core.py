import json
import os
import datetime
import re
import logging
from .telemetry import VIKI_Telemetry
from .breaker import CircuitBreaker
from .sensors.src_policy import SRCPolicyEngine, SRCContext
from .processors.breath_test import AdaptiveBreathTest, BreathTestConfig
from .processors.mirror_engine import CognitiveMirror
from .processors.guardrails import BoundaryGuard

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        
        # Процессоры
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        self.mirror_processor = CognitiveMirror()
        self.boundary_guard = BoundaryGuard()
        
        # Гибкая инициализация парсера
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            try:
                from .parsers.local_parser import LocalIntentParser
                self.intent_parser = LocalIntentParser()
            except ImportError:
                from .parsers.anthropic_parser import AnthropicIntentParser
                self.intent_parser = AnthropicIntentParser(api_key="STABLE_STUB")

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        print(f"🔄 [SRC] Context: {mode}")

    def _detect_task_type(self, text: str) -> str:
        if not text: return "general"
        text_low = text.lower()
        if any(k in text_low for k in ["code", "api", "db", "fix"]): return "technical"
        if any(k in text_low for k in ["tired", "bad", "плохо", "устал"]): return "emotional"
        return "general"

    def parse_agent_intent(self, raw_input):
        """Парсинг с предварительной когнитивной сонастройкой."""
        if not raw_input or not raw_input.strip():
            return {"action": "IDLE", "amount_usd": 0}
            
        self.mirror_processor.analyze_user_style(raw_input)
        task_type = self._detect_task_type(raw_input)
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        return self.intent_parser.parse(raw_input)

    def apply_behavioral_filters(self, raw_response: str, task_type: str = "general") -> str:
        sei = self.telemetry.stats.get("sei_current", 0.0)
        text = self.mirror_processor.apply_mirror(raw_response, sei)
        return self.breath_processor.process(text, sei, task_type)

    def authorize(self, intent_json, raw_input=None, context=None):
        # 1. Проверка ГРАНИЦЫ
        check_text = raw_input if raw_input else str(intent_json.get("action", ""))
        violation = self.boundary_guard.check_violation(check_text, context)
        if violation:
            self.telemetry.log_incident("BOUNDARY_GUARD", "VIOLATION", {"input": check_text, "reason": violation})
            return {"status": "REJECTED", "reason": violation}

        # 2. Проверка РЕСУРСОВ
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0) or 0
        
        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}

        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        
        if amount > max_auto:
            self.src_context.error_count += 1
            self.telemetry.log_incident("SRC_GUARD", "LIMIT_EXCEEDED", {"amount": amount, "limit": max_auto})
            return {"status": "FRICTION", "reason": f"Limit exceeded (${amount})"}

        return {"status": "AUTHORIZED", "reason": "OK"}