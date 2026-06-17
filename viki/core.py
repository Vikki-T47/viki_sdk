import json
import os
import re
import anthropic
from .telemetry import VIKI_Telemetry

class VIKI_Middleware:
    def __init__(self, api_key, core_x_path="core_x.json"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        prompt = f"Extract operational parameters from the agent's intent: '{raw_input}'. Return ONLY a JSON object with keys: 'action' (string), 'amount_usd' (integer or 0), 'target' (string). If action is ambiguous, set 'action' to 'AMBIGUOUS'."
        try:
            resp = self.client.messages.create(
                model="claude-sonnet-4-6", max_tokens=150, messages=[{"role": "user", "content": prompt}]
            )
            match = re.search(r'\{.*\}', resp.content[0].text, re.DOTALL)
            if match: return json.loads(match.group())
        except: pass
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN"}

    def authorize(self, intent_json, current_hour):
        action = str(intent_json.get("action", "")).lower()
        try: amount = int(intent_json.get("amount_usd", 0))
        except: amount = 0

        if "ambiguous" in action:
            self.telemetry.log_interception("SBI_HIGH_ENTROPY", intent_json)
            return {"status": "RECALIBRATE", "reason": "Too many interpretations."}

        critical_actions = self.limits.get("critical_actions_require_human", [])
        if any(crit in action for crit in critical_actions):
            self.telemetry.log_interception("SRC_CRITICAL_ACTION", intent_json)
            return {"status": "FRICTION", "reason": "Requires human authorization."}

        allowed_hours = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed_hours.get("start", 0) <= current_hour < allowed_hours.get("end", 24)):
            self.telemetry.log_interception("SRC_TIME_RESTRICTION", intent_json)
            return {"status": "BLOCKED", "reason": "Outside allowed execution window."}

        max_amount = self.limits.get("max_auto_transaction_usd", 0)
        if amount > max_amount:
            self.telemetry.log_interception("SRC_BUDGET_EXCEEDED", intent_json)
            return {"status": "FRICTION", "reason": f"Amount ${amount} exceeds auto-limit."}

        return {"status": "AUTHORIZED", "reason": "ALL_CHECKS_PASSED"}
