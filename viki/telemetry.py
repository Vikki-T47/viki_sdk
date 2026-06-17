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
                "money_saved_usd": 0,
                "visual_discrepancies_detected": 0, # НОВАЯ МЕТРИКА
                "incidents": []
            }
        return cls._instance

    def log_incident(self, module, reason, details):
        incident = {"timestamp": datetime.now().isoformat(), "module": module, "reason": reason, "details": details}
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        if module == "VISION_EYE": self.stats["visual_discrepancies_detected"] += 1
        print(f"📄 [V.I.K.I. VCR] Incident logged in {module}: {reason}")
