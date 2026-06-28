import json
import logging
import time
import os
from datetime import datetime
from .sensors.sei_sensor import EntropySensor

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0, "tokens_saved": 0, "money_saved_usd": 0,
                "operator_time_saved_min": 0, "incidents": [], "sei_current": 0.0,
                "last_sei_update": time.time(), "memory_sync_events": 0 
            }
            cls._instance.sei_sensor = EntropySensor(history_window=5)
            cls._instance.live_log_path = "viki_live.md"
        return cls._instance

    def log_incident(self, module, reason, details):
        """Запись инцидента в базу и в живой Markdown-лог."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 1. Запись в системную статистику
        incident = {"timestamp": timestamp, "module": module, "reason": reason, "details": str(details)}
        self.stats["incidents"].append(incident)
        if reason != "STATE_OVERWRITE": self.stats["total_blocks"] += 1

        # 2. ПРОТОКОЛ «СВЕТ»: Запись в viki_live.md
        status_emoji = "🛑" if "GUARD" in module or "BOUNDARY" in module else "⚠️"
        if reason == "SYNCED": status_emoji = "✅"
        if reason == "STATE_OVERWRITE": status_emoji = "🧹"
        
        log_entry = f"| {timestamp} | {module} | {status_emoji} {reason} | {str(details)} |\n"
        
        try:
            with open(self.live_log_path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except: pass

    def trigger_rest(self):
        self.sei_sensor.cool_down()
        self.stats["sei_current"] = 0.0
        self.log_incident("CORE", "REST_ACTIVATED", "Affective state fully reset.")

    def update_sei(self, user_input, context=None):
        if user_input and isinstance(user_input, str) and user_input.strip():
            self.sei_sensor.update(user_input, context)
            self.stats["sei_current"] = self.sei_sensor.calculate()
        return self.stats["sei_current"]

class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
    def authorize_next_step(self, expected, actual, probe_type="GENERIC"):
        delta = abs(expected - actual)
        return {"status": "SYNCED" if delta <= (expected * self.tolerance) else "HALT", "probe": probe_type}