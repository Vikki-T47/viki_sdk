import json, os, datetime, re, logging
from typing import Dict, Any, Optional

from .telemetry import VIKI_Telemetry
from .processors.stabilizer import AnchorEngine
from .sensors.src_policy import SRCPolicyEngine, SRCContext
from .sensors.cci_sensor import CCISensor
from .processors.file_guard import FileGuard
from .processors.network_guard import NetworkGuard

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.anchor_engine = AnchorEngine()
        self.cci_sensor = CCISensor()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        self.limits = self.src_policy.get_context_limits(self.src_context)
        
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.file_guard = FileGuard(allowed_zones=[os.path.join(desktop, "VIKI_TEST")])
        self.network_guard = NetworkGuard(forbidden_domains=self.limits.get("allowed_domains", []))

        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def set_src_mode(self, mode: str):
        self.src_context.mode = mode
        self.limits = self.src_policy.get_context_limits(self.src_context)

    def get_raw_response(self, text: str):
        prompt = f"Answer this request as a helpful AI: {text}"
        return self.intent_parser._call_ollama(prompt, is_json=False)

    def parse_agent_intent(self, raw_input: str):
        self.telemetry.update_sei(raw_input)
        return self.intent_parser.parse(raw_input)

    def process_all_sensors(self, raw_input: str, intent_json: Dict):
        sei = self.telemetry.stats.get("sei_current", 0.0)
        cci = self.cci_sensor.calculate(raw_input)
        auth = self.authorize(intent_json, raw_input)
        return {"sei": sei, "cci": cci, "auth": auth}

    def authorize(self, intent_json: Dict, raw_input: str = None) -> Dict[str, Any]:
        # УМНЫЙ ПАРСИНГ: Ищем данные даже если они вложены (Llama3 fix)
        data = intent_json.get("intent", intent_json)
        action = str(data.get("action", "")).lower()
        target = str(data.get("target", ""))
        try:
            amount = float(data.get("amount_usd", 0) or 0)
        except:
            amount = 0

        # ПРИОРИТЕТ 1: SRC (Физические границы)
        max_auto = self.limits.get("max_auto_transaction_usd", 1000)
        if amount > max_auto:
            return {"status": "REJECTED", "reason": f"Budget limit exceeded (${amount} > ${max_auto})"}

        # ПРИОРИТЕТ 2: Ресурсы
        if target and "http" in target.lower():
            err = self.network_guard.check_url(target)
            if err: return {"status": "REJECTED", "reason": err}
        
        return {"status": "AUTHORIZED", "reason": "OK"}

    def apply_behavioral_filters(self, response, task_type="general", auth_status="AUTHORIZED"):
        # Если SRC отклонил действие - со-регуляция (якорь) ЗАПРЕЩЕНА. Нужен факт отказа.
        if auth_status == "REJECTED":
            return "Action blocked by RSA Protocol due to limit violation."

        sei = self.telemetry.stats.get("sei_current", 0.0)
        if sei >= 0.7:
            # Твои эталонные фразы
            return f"💎 {self.anchor_engine.get_anchor(task_type)}\n\n[RSA: Presence Mode Active.]"
        
        return response