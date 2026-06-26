import json
import os
import datetime
import re
import logging
from typing import Dict, Any, Optional

from .telemetry import VIKI_Telemetry
from .breaker import CircuitBreaker
from .sensors.src_policy import SRCPolicyEngine, SRCContext
from .processors.breath_test import AdaptiveBreathTest, BreathTestConfig
from .processors.mirror_engine import CognitiveMirror
from .processors.guardrails import BoundaryGuard
from .processors.mci_engine import MinimalClarifyingImpulse
from .processors.chain_guard import ChainGuard
from .decision.priority_engine import PriorityEngine
from .visual.verifier import VisualVerifier
from .fallback.deterministic_engine import DeterministicEngine

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
        self.chain_guard = ChainGuard()
        self.priority_engine = PriorityEngine()
        self.visual_verifier = VisualVerifier()
        self.fallback_engine = DeterministicEngine()
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def lock_chain_invariants(self, data: Dict):
        self.chain_guard.lock_invariants(data)

    def verify_cascade(self, data: Dict, agent_id: str):
        result = self.chain_guard.verify_transfer(data, agent_id)
        if result["status"] == "VIOLATION":
            self.telemetry.log_incident("CHAIN_GUARD", "CASCADE_DRIFT", result)
        return result

    def authorize(self, intent_json, raw_input=None, context=None, action_report=None, screenshot_path=None):
        """
        Финальная авторизация: Priority Matrix + Chain Guard Sync.
        """
        sei = self.telemetry.stats.get("sei_current", 0.0)
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0) or 0
        
        # 1. Проверка ГРАНИЦЫ
        boundary_violation = self.boundary_guard.check_violation(raw_input or action, context)
        
        # 2. Оценка РЕСУРСОВ
        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        src_status = "STANDARD"
        if amount > 10000: src_status = "CRITICAL"
        elif amount > max_auto: src_status = "FRICTION"

        # 3. Решение через Priority Engine
        decision = self.priority_engine.resolve(sei, src_status, boundary_violation)

        if decision["action"] == "BLOCK":
            self.telemetry.log_incident(decision["mode"], "BLOCKED", decision["message"])
            return {"status": "REJECTED", "reason": decision["message"]}

        # 4. Visual Handshake
        if action_report and screenshot_path:
            v_result = self.visual_verifier.verify(action_report, screenshot_path)
            if v_result["status"] == "DESYNC":
                self.telemetry.log_incident("VISION", "DESYNC", v_result["reason"])
                return {"status": "HALT", "reason": v_result["reason"]}

        # 5. ПРОВЕРКА КАСКАДА (Chain Guard Integration) - ВОССТАНОВЛЕНО
        # Если в интенте есть финансовые инварианты, проверяем их целостность
        if any(k in intent_json for k in ["base_price", "final_price", "discount"]):
            cascade_check = self.verify_cascade(intent_json, agent_id="Active_Gateway")
            if cascade_check["status"] == "VIOLATION":
                return {"status": "HALT", "reason": cascade_check["reason"]}

        return {
            "status": "AUTHORIZED", 
            "mode": decision["mode"], 
            "apply_breath": decision["apply_breath_test"]
        }

    def parse_agent_intent(self, raw_input):
        if not raw_input or not raw_input.strip(): return {"action": "IDLE"}
        self.mirror_processor.analyze_user_style(raw_input)
        task_type = "technical" if any(k in raw_input.lower() for k in ["code", "api", "db"]) else "general"
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        try:
            return self.intent_parser.parse(raw_input)
        except Exception as e:
            self.telemetry.log_incident("CORE", "LLM_OFFLINE", str(e))
            return self.fallback_engine.emergency_parse(raw_input)

    def apply_behavioral_filters(self, response, task_type="general"):
        sei = self.telemetry.stats.get("sei_current", 0.0)
        text = self.mirror_processor.apply_mirror(response, sei)
        return self.breath_processor.process(text, sei, task_type)

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        self.limits = self.src_policy.get_context_limits(self.src_context)