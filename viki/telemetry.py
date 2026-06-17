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
                "incidents": [] 
            }
        return cls._instance

    def log_incident(self, module, reason, details):
        incident = {
            "timestamp": datetime.now().isoformat(),
            "module": module,
            "reason": reason,
            "agent_intent": details,
            "status": "HALTED_BY_VIKI"
        }
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        self.stats["tokens_saved"] += 1500
        self.stats["operator_time_saved_min"] += 30
        self.stats["money_saved_usd"] += details.get("amount_usd", 0) if isinstance(details, dict) else 0
        print(f"📄 [VCR] Incident logged: {reason}")
