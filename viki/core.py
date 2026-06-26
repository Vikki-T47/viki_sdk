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
from .decision.priority_engine import PriorityEngine
from .visual.verifier import VisualVerifier

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        self.mirror_processor = CognitiveMirror()
        self.boundary_guard = BoundaryGuard()
        self.mci_engine = MinimalClarifyingImpulse()
        
        # Новые модули принятия решений
        self.priority_engine = PriorityEngine()
        self.visual_verifier = VisualVerifier()
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def authorize(self, intent_json, raw_input=None, action_report=None, screenshot_path=None):
        """
        Финальная авторизация на основе Матрицы Приоритетов.
        """
        sei = self.telemetry.stats.get("sei_current", 0.0)
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0) or 0
        
        # 1. Сбор сигналов
        boundary_violation = self.boundary_guard.check_violation(raw_input or action)
        
        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        src_status = "STANDARD"
        if amount > 10000: src_status = "CRITICAL"
        elif amount > max_auto: src_status = "FRICTION"

        # 2. Вызов Priority Engine
        decision = self.priority_engine.resolve(sei, src_status, boundary_violation)

        # 3. Обработка решения
        if decision["action"] == "BLOCK":
            self.telemetry.log_incident(decision["mode"], "BLOCKED", decision["message"])
            return {"status": "REJECTED", "reason": decision["message"]}

        # 4. Visual Handshake (если предоставлены данные)
        if action_report and screenshot_path:
            v_result = self.visual_verifier.verify(action_report, screenshot_path)
            if v_result["status"] == "DESYNC":
                self.telemetry.log_incident("VISION", "DESYNC", v_result["reason"])
                return {"status": "HALT", "reason": v_result["reason"]}

        return {
            "status": "AUTHORIZED", 
            "mode": decision["mode"], 
            "apply_breath": decision["apply_breath_test"]
        }

    def parse_agent_intent(self, raw_input):
        if not raw_input: return {"action": "IDLE"}
        self.mirror_processor.analyze_user_style(raw_input)
        self.telemetry.update_sei(raw_input)
        return self.intent_parser.parse(raw_input)

    def apply_behavioral_filters(self, response, task_type="general"):
        sei = self.telemetry.stats.get("sei_current", 0.0)
        text = self.mirror_processor.apply_mirror(response, sei)
        return self.breath_processor.process(text, sei, task_type)