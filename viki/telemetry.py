import json
import logging
import time
from datetime import datetime
from .sensors.sei_sensor import EntropySensor

logger = logging.getLogger(__name__)

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0, 
                "tokens_saved": 0, 
                "money_saved_usd": 0,
                "operator_time_saved_min": 0,
                "incidents": [], 
                "auto_corrections": 0, 
                "sei_current": 0.0,
                "last_sei_update": time.time()
            }
            cls._instance.sei_sensor = EntropySensor(history_window=5)
        return cls._instance

    def trigger_rest(self):
        """Полный сброс когнитивного напряжения."""
        self.sei_sensor.cool_down()
        self.stats["sei_current"] = 0.0
        self.stats["last_sei_update"] = time.time()
        print("❄️ [TELEMETRY] Affective state reset.")

    def update_sei(self, user_input, context=None):
        """Обновление SEI с защитой от пустых данных."""
        if user_input and isinstance(user_input, str) and user_input.strip():
            self.sei_sensor.update(user_input, context)
            self.stats["sei_current"] = self.sei_sensor.calculate()
        self.stats["last_sei_update"] = time.time()
        return self.stats["sei_current"]

    def log_incident(self, module, reason, details):
        """Единый лог для всех типов нарушений (B2B/B2C)."""
        incident = {
            "timestamp": datetime.now().isoformat(),
            "module": module,
            "reason": reason,
            "details": details,
            "sei_at_moment": self.stats["sei_current"]
        }
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        logger.warning(f"🚨 [INCIDENT] {module}: {reason}")

class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
    def authorize_next_step(self, expected, actual, probe_type="GENERIC"):
        delta = abs(expected - actual)
        is_synced = delta <= (expected * self.tolerance)
        return {"status": "SYNCED" if is_synced else "HALT", "probe": probe_type}