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

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        self.limits = self.src_policy.get_context_limits(self.src_context)
        
        # Процессоры вывода
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        self.mirror_processor = CognitiveMirror()
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.src_context.scenario = scenario
        self.limits = self.src_policy.get_context_limits(self.src_context)

    def _detect_task_type(self, text: str) -> str:
        text_low = text.lower()
        if any(k in text_low for k in ["code", "api", "fix", "db"]): return "technical"
        if any(k in text_low for k in ["tired", "bad", "sad", "устал", "плохо"]): return "emotional"
        return "general"

    def parse_agent_intent(self, raw_input):
        # 1. Сначала анализируем СТИЛЬ для зеркалирования
        self.mirror_processor.analyze_user_style(raw_input)
        
        # 2. Обновляем SEI и контекст
        task_type = self._detect_task_type(raw_input)
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        
        return self.intent_parser.parse(raw_input)

    def apply_behavioral_filters(self, raw_response: str, task_type: str = "general") -> str:
        """
        Комплексная мутация сигнала: Mirroring + Breath Test.
        """
        sei = self.telemetry.stats.get("sei_current", 0.0)
        
        # ШАГ 1: Когнитивное Зеркалирование (Подстройка под темп)
        text = self.mirror_processor.apply_mirror(raw_response, sei)
        
        # ШАГ 2: Адаптивное Дыхание (Безопасность и плотность)
        text = self.breath_processor.process(text, sei, task_type)
        
        return text

    def authorize(self, intent_json, token_id=None):
        amount = intent_json.get("amount_usd", 0)
        if amount is None: amount = 0
        
        action = str(intent_json.get("action", "")).lower()
        current_limits = self.src_policy.get_context_limits(self.src_context)

        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}

        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            self.src_context.error_count += 1
            return {"status": "FRICTION", "reason": f"Limit exceeded (${amount})"}

        return {"status": "AUTHORIZED", "reason": "OK"}