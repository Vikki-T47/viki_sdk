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
from .processors.mci_engine import MinimalClarifyingImpulse

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        self.limits = self.src_policy.get_context_limits(self.src_context)
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        self.mirror_processor = CognitiveMirror()
        self.boundary_guard = BoundaryGuard()
        self.mci_engine = MinimalClarifyingImpulse()
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def parse_agent_intent(self, raw_input):
        if not raw_input or not raw_input.strip(): return {"action": "IDLE", "amount_usd": 0}
        self.mirror_processor.analyze_user_style(raw_input)
        task_type = "technical" if any(k in raw_input.lower() for k in ["code", "api", "db"]) else "general"
        if any(k in raw_input.lower() for k in ["tired", "bad", "устал", "плохо"]): task_type = "emotional"
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        return self.intent_parser.parse(raw_input)

    def apply_behavioral_filters(self, raw_response: str, task_type: str = "general") -> str:
        sei = self.telemetry.stats.get("sei_current", 0.0)
        text = self.mirror_processor.apply_mirror(raw_response, sei)
        return self.breath_processor.process(text, sei, task_type)

    def authorize(self, intent_json, raw_input=None, context=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0) or 0
        target = str(intent_json.get("target", "")).upper().strip()

        # 1. Проверка ГРАНИЦЫ
        check_text = raw_input if raw_input else action
        violation = self.boundary_guard.check_violation(check_text, context)
        if violation: return {"status": "REJECTED", "reason": violation}

        # 2. РАСШИРЕННЫЙ MCI (Валидация ТАРГЕТА)
        # ИСПРАВЛЕНО: Список слов, которые НЕ могут быть получателем
        invalid_targets = ["USD", "EUR", "MONEY", "UNKNOWN", "SOMEONE", "ANY", ""]
        
        if "ambiguous" in action or not action:
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("general")}
        
        if amount == 0 and "transfer" in action:
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("amount")}
            
        if target in invalid_targets and "transfer" in action:
            # Если агент вписал валюту вместо имени — требуем уточнения
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("target")}

        # 3. ПРОВЕРКА РЕСУРСОВ
        if not self.breaker.can_execute(action): return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}
        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        
        if amount > max_auto:
            self.src_context.error_count += 1
            return {"status": "FRICTION", "reason": f"Limit exceeded (${amount})"}

        return {"status": "AUTHORIZED", "reason": "OK"}

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        self.limits = self.src_policy.get_context_limits(self.src_context)