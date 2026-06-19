import json
import os
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()

    @classmethod
    def with_anthropic(cls, api_key, core_x_path="core_x.json"):
        from .parsers.anthropic_parser import AnthropicIntentParser
        parser = AnthropicIntentParser(api_key)
        return cls(parser, core_x_path)

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        return self.intent_parser.parse(raw_input)

    def authorize(self, intent_json, token_id=None):
        # ... (предыдущие проверки: бюджет, критические действия) ...
        
        # НОВОЕ: Сверка с живым контекстом
        from .sensors import RealityProbe
        probe = RealityProbe()
        
        # Если агент хочет сделку - проверяем квоту API
        is_quota_ok, quota_msg = probe.check_api_quota("BANK_GATEWAY")
        if not is_quota_ok:
            self.telemetry.log_incident("SRC_GUARD", "QUOTA_EXHAUSTED", intent_json)
            return {"status": "BLOCKED", "reason": quota_msg}
            
        return {"status": "AUTHORIZED", "reason": "REALITY_SYNC_COMPLETE"}