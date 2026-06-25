import json
import os
import datetime
import re
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController
from .breaker import CircuitBreaker

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            try:
                from .parsers.local_parser import LocalIntentParser
                self.intent_parser = LocalIntentParser()
            except ImportError:
                from .parsers.anthropic_parser import AnthropicIntentParser
                self.intent_parser = AnthropicIntentParser(api_key="STABLE_STUB")

        self.interrupt_controller = RealityInterruptController()
        self.breaker = CircuitBreaker()

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def _detect_task_type(self, text: str) -> str:
        tech_keywords = ["code", "api", "database", "fix", "deploy"]
        return "technical" if any(k in text.lower() for k in tech_keywords) else "general"

    def parse_agent_intent(self, raw_input):
        context = {"task_type": self._detect_task_type(raw_input)}
        self.telemetry.update_sei(raw_input, context)
        return self.intent_parser.parse(raw_input)

    def apply_breath_test(self, raw_response):
        """Физика со-регуляции. ИСПРАВЛЕНО: Снижен порог до 0.30."""
        sei = self.telemetry.stats["sei_current"]
        
        # Если энтропия выше 0.30 — начинаем мягкое сжатие
        if sei >= 0.30:
            clean_text = re.sub(r'\?+', '.', raw_response)
            sentences = [s.strip() for s in clean_text.split('.') if s.strip()]
            
            # При критической энтропии (0.6+) - жесткое сжатие
            limit = 1 if sei > 0.6 else 2
            final_text = ". ".join(sentences[:limit]) + "."
            
            return f"{final_text}\n\n[RSA: Cognitive Load Detected. Presence Mode Active.]"
        
        return raw_response

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN"}
        max_auto = self.limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            return {"status": "FRICTION", "reason": f"Limit exceeded (${amount})"}
        return {"status": "AUTHORIZED", "reason": "OK"}