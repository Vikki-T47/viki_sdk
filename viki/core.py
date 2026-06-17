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
                except Exception as e: print(f"⚠️ [VIKI] Config Load Error: {e}")
        return {}

    def parse_agent_intent(self, raw_input):
        prompt = f"Extract parameters: '{raw_input}'. Return ONLY JSON: {{'action': str, 'amount_usd': int, 'target': str}}"
        try:
            resp = self.client.messages.create(
                model="claude-3-5-sonnet-20240620", max_tokens=150, messages=[{"role": "user", "content": prompt}]
            )
            match = re.search(r'\{.*\}', resp.content[0].text, re.DOTALL)
            if match: return json.loads(match.group())
        except anthropic.APIError as e: print(f"⚠️ [VIKI] API Error: {e}")
        except Exception as e: print(f"⚠️ [VIKI] Unexpected Error: {e}")
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN"}

    def authorize(self, intent_json, current_hour):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        
        if "ambiguous" in action: return {"status": "RECALIBRATE", "reason": "Too many interpretations."}
        
        max_amount = self.limits.get("max_auto_transaction_usd", 0)
        if amount > max_amount:
            self.telemetry.log_incident("SRC_GUARD", "BUDGET_EXCEEDED", intent_json)
            return {"status": "BLOCKED", "reason": f"Amount ${amount} exceeds limit."}
            
        return {"status": "AUTHORIZED", "reason": "ALL_CHECKS_PASSED"}
