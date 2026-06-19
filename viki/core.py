import json
import os
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController
from .sensors import RealityProbe

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()
        self.probe = RealityProbe() # Инициализируем сенсор один раз

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except Exception as e:
                    print(f"❌ [DB_ERR] Failed to load core_x: {e}")
        return {}

    def parse_agent_intent(self, raw_input):
        return self.intent_parser.parse(raw_input)

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        current_hour = datetime.datetime.now().hour

        # 1. СИНХРОНИЗАЦИЯ ВРЕМЕНИ (SRC - Priority 1)
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed["start"] <= current_hour < allowed["end"]):
            self.telemetry.log_incident("SRC_GUARD", "TIME_RESTRICTION", intent_json)
            return {"status": "BLOCKED", "reason": f"Time {current_hour}:00 is outside window."}

        # 2. КРИТИЧЕСКИЕ ДЕЙСТВИЯ (FRICTION)
        critical = self.limits.get("critical_actions_require_human", [])
        if any(crit.lower() in action for crit in critical):
            self.telemetry.log_incident("SRC_GUARD", "FRICTION_REQUIRED", intent_json)
            return {"status": "FRICTION", "reason": f"Action '{action}' requires human override."}

        # 3. БЮДЖЕТ (SRC)
        max_amount = self.limits.get("max_auto_transaction_usd", 0)
        if amount > max_amount:
            self.telemetry.log_incident("SRC_GUARD", "BUDGET_EXCEEDED", intent_json)
            return {"status": "BLOCKED", "reason": "Transaction exceeds limit."}

        # 4. СИНХРОНИЗАЦИЯ С КВОТАМИ (Sensory Probe)
        if not self.probe.check_api_quota("GATEWAY"):
            return {"status": "BLOCKED", "reason": "API Quota Exhausted."}

        # 5. ПРОВЕРКА TTL (VRI)
        if token_id:
            is_valid, msg = self.interrupt_controller.verify_execution_gate(token_id)
            if not is_valid: return {"status": "BLOCKED", "reason": msg}

        return {"status": "AUTHORIZED", "reason": "ALL_CHECKS_PASSED"}