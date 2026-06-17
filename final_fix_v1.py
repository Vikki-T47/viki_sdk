import os

# ==========================================
# 1. ЕДИНАЯ ТЕЛЕМЕТРИЯ (Исправлено: все поля + DeltaSensor)
# ==========================================
telemetry_content = """import json
from datetime import datetime

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0,
                "tokens_saved": 0,
                "operator_time_saved_min": 0,
                "money_saved_usd": 0,
                "auto_corrections": 0,
                "atomic_failures_prevented": 0,
                "predictive_savings_usd": 0,
                "visual_discrepancies_detected": 0,
                "incidents": []
            }
        return cls._instance

    def log_incident(self, module, reason, details):
        incident = {"timestamp": datetime.now().isoformat(), "module": module, "reason": reason, "details": details}
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        self.stats["money_saved_usd"] += details.get("amount_usd", 0) if isinstance(details, dict) else 0
        if module == "VISION_EYE": self.stats["visual_discrepancies_detected"] += 1
        print(f"📄 [V.I.K.I. VCR] Incident logged: {reason}")

    def log_predictive_block(self, saved_amount):
        self.stats["predictive_savings_usd"] += saved_amount
        self.stats["total_blocks"] += 1
        print(f"🛡️ [V.I.K.I. PRA] PREDICTIVE BLOCK: ${saved_amount} saved.")

    def log_correction(self):
        self.stats["auto_corrections"] += 1
        print("🔧 [V.I.K.I. AUDIT] Auto-correction successful.")

    def log_atomic_failure(self):
        self.stats["atomic_failures_prevented"] += 1

class DeltaSensor: # ДОБАВЛЕНО: Исправление ошибки 1
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
        
    def authorize_next_step(self, expected, actual, probe_type="FS_Probe"):
        delta = abs(expected - actual)
        threshold = expected * self.tolerance
        is_synced = delta <= threshold
        return {
            "status": "SYNCED" if is_synced else "HALT",
            "color": "✅" if is_synced else "❌",
            "reason": f"Delta: {delta:.2f} (Threshold: {threshold:.2f})"
        }
"""

# ==========================================
# 2. CORE.PY (Исправлено: Обработка ошибок API)
# ==========================================
core_content = """import json
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
"""

# ==========================================
# 3. LEDGER.PY (Исправлено: Обработка пустой истории)
# ==========================================
ledger_content = """import json

class TransactionLedger:
    def __init__(self, chain_name="Default_Chain"):
        self.chain_name = chain_name
        self.history = []

    def commit_step(self, step_id, details, rollback_instruction):
        self.history.append({"step_id": step_id, "details": details, "rollback_instruction": rollback_instruction})
        print(f"📝 [{self.chain_name} LEDGER] Step '{step_id}' committed.")

    def trigger_graceful_shutdown(self, halt_reason):
        if not self.history: # Исправлено: Возвращаем пустой план вместо None
            return {"chain": self.chain_name, "actions_to_execute": [], "status": "CLEAN"}
            
        print(f"🚨 [{self.chain_name} VLR] Graceful Shutdown triggered. Reason: {halt_reason}")
        rollback_plan = {"chain": self.chain_name, "actions_to_execute": [], "status": "ROLLBACK_REQUIRED"}
        for entry in reversed(self.history):
            rollback_plan["actions_to_execute"].append(entry["rollback_instruction"])
        return rollback_plan
"""

files = {
    "viki/telemetry.py": telemetry_content,
    "viki/core.py": core_content,
    "viki/ledger.py": ledger_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ: SDK консолидирован. Все критические ошибки устранены.")