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
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()
        # ИСПРАВЛЕНО: Предохранитель теперь на месте
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

    def apply_breath_test(self, raw_response):
        """
        Физика со-регуляции. Сжимает ответ ИИ при высоком SEI.
        """
        sei = self.telemetry.stats["sei_current"]
        
        if sei >= 0.7:
            # 1. Удаляем все вопросы (Zero-Question Policy)
            clean_text = re.sub(r'\?+', '.', raw_response)
            
            # 2. ИСПРАВЛЕНО: Умное сжатие (по точкам или по длине)
            sentences = [s.strip() for s in clean_text.split('.') if s.strip()]
            
            if len(sentences) >= 2:
                final_text = ". ".join(sentences[:2]) + "."
            elif len(clean_text) > 100:
                final_text = clean_text[:100].strip() + "..."
            else:
                final_text = clean_text
                
            final_text += "\n\n[RSA: System in PRESENCE mode. Space opened.]"
            return final_text
        
        return raw_response

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        
        # ИСПРАВЛЕНО: Теперь Breaker реально проверяет возможность действия
        if not self.breaker.can_execute(action):
            return {"status": "BLOCKED", "reason": "CIRCUIT_OPEN: Target service isolated."}
            
        amount = intent_json.get("amount_usd", 0)
        max_auto = self.limits.get("max_auto_transaction_usd", 1000)
        
        if amount > max_auto:
            return {"status": "FRICTION", "reason": "High weight transaction."}
            
        return {"status": "AUTHORIZED", "reason": "OK"}