import json
import logging
import time
from datetime import datetime
from .sensors.sei_sensor import EntropySensor

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0, 
                "tokens_saved": 0, 
                "money_saved_usd": 0,
                "operator_time_saved_min": 0, # ЭТОТ КЛЮЧ БЫЛ ПРОПУЩЕН
                "incidents": [], 
                "auto_corrections": 0, 
                "sei_current": 0.0,
                "last_sei_update": time.time()
            }
            cls._instance.sei_sensor = EntropySensor(history_window=5)
        return cls._instance

    def trigger_rest(self):
        """Сброс аффективного состояния."""
        self.sei_sensor.cool_down()
        self.stats["sei_current"] = 0.0
        self.stats["last_sei_update"] = time.time()
        print(f"❄️ [TELEMETRY] Affective state fully reset.")

    def update_sei(self, user_input, context=None):
        if user_input and user_input.strip():
            self.sei_sensor.update(user_input, context)
            self.stats["sei_current"] = self.sei_sensor.calculate()
        self.stats["last_sei_update"] = time.time()
        return self.stats["sei_current"]

    def log_incident(self, module, reason, details):
        incident = {
            "timestamp": datetime.now().isoformat(), 
            "module": module, 
            "reason": reason, 
            "details": details, 
            "sei": self.stats["sei_current"]
        }
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1

class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
    def authorize_next_step(self, expected, actual):
        delta = abs(expected - actual)
        return {"status": "SYNCED" if delta <= (expected * self.tolerance) else "HALT"}