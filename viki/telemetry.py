import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0, "tokens_saved": 0, "money_saved_usd": 0,
                "incidents": [], "auto_corrections": 0, "sei_current": 0.0
            }
        return cls._instance

    def calculate_sei(self, user_input):
        """
        Subject Entropy Index (SEI) Calculation.
        """
        # ИСПРАВЛЕНО: Проверка на None и корректность типа
        if user_input is None or not isinstance(user_input, str):
            return 0.0
            
        text = user_input.strip()
        if not text: return 0.0
        
        entropy_score = 0.0
        if text.islower(): entropy_score += 0.3
        if len(text.split()) < 3: entropy_score += 0.3
        
        affect_markers = ["устал", "плохо", "бесполезно", "надоело", "хватит", "бесит"]
        if any(m in text.lower() for m in affect_markers):
            entropy_score += 0.4
            
        self.stats["sei_current"] = min(entropy_score, 1.0)
        logger.info(f"🧠 [SEI SENSOR] Subject Entropy: {self.stats['sei_current']}")
        return self.stats["sei_current"]

    def log_incident(self, module, reason, details):
        incident = {"timestamp": datetime.now().isoformat(), "module": module, "reason": reason, "details": details}
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        print(f"📄 [VCR] Incident logged: {module} -> {reason}")

class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
    def authorize_next_step(self, expected, actual):
        delta = abs(expected - actual)
        is_synced = delta <= (expected * self.tolerance)
        return {"status": "SYNCED" if is_synced else "HALT"}