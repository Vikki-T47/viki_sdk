import json
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
