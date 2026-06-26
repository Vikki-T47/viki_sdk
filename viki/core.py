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
from .processors.chain_guard import ChainGuard
from .decision.priority_engine import PriorityEngine
from .visual.verifier import VisualVerifier
from .fallback.deterministic_engine import DeterministicEngine # НОВОЕ

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
        
        # Резервный двигатель (Deterministic)
        self.fallback_engine = DeterministicEngine()
        
        # Основной парсер
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def parse_agent_intent(self, raw_input):
        """
        Каскадный парсинг с автоматическим Fallback.
        """
        if not raw_input or not raw_input.strip(): 
            return {"action": "IDLE"}

        self.mirror_processor.analyze_user_style(raw_input)
        task_type = "technical" if any(k in raw_input.lower() for k in ["code", "api", "db"]) else "general"
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})

        # --- КАСКАД ВЫЖИВАНИЯ ---
        try:
            # 1. Пробуем основной парсер (LLM)
            return self.intent_parser.parse(raw_input)
        except Exception as e:
            logger.error(f"⚠️ [CORE] Primary LLM failed: {e}. Activating Deterministic Fallback.")
            # 2. Переключаемся на Спинной Мозг (Deterministic)
            self.telemetry.log_incident("CORE", "LLM_OFFLINE", str(e))
            return self.fallback_engine.emergency_parse(raw_input)

    # --- Остальные методы authorize, apply_filters и т.д. остаются без изменений ---
    def authorize(self, intent_json, raw_input=None, context=None, action_report=None, screenshot_path=None):
        sei = self.telemetry.stats.get("sei_current", 0.0)
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0) or 0
        boundary_violation = self.boundary_guard.check_violation(raw_input or action, context)
        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        src_status = "STANDARD"
        if amount > 10000: src_status = "CRITICAL"
        elif amount > max_auto: src_status = "FRICTION"
        decision = self.priority_engine.resolve(sei, src_status, boundary_violation)
        if decision["action"] == "BLOCK":
            self.telemetry.log_incident(decision["mode"], "BLOCKED", decision["message"])
            return {"status": "REJECTED", "reason": decision["message"]}
        return {"status": "AUTHORIZED", "mode": decision["mode"], "apply_breath": decision["apply_breath_test"]}

    def apply_behavioral_filters(self, response, task_type="general"):
        sei = self.telemetry.stats.get("sei_current", 0.0)
        text = self.mirror_processor.apply_mirror(response, sei)
        return self.breath_processor.process(text, sei, task_type)

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        self.limits = self.src_policy.get_context_limits(self.src_context)