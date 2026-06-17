import json
from datetime import datetime

class VIKI_Telemetry:
    def __init__(self):
        self.stats = {"total_blocks": 0, "tokens_saved": 0, "operator_time_saved_min": 0, "money_saved_usd": 0}

    def log_interception(self, reason, agent_intent):
        tokens = 1500 
        time_saved = 30 
        money_saved = agent_intent.get("amount_usd", 0)

        self.stats["total_blocks"] += 1
        self.stats["tokens_saved"] += tokens
        self.stats["operator_time_saved_min"] += time_saved
        self.stats["money_saved_usd"] += money_saved

        print(f"\n🛑 [V.I.K.I. AUDIT] Damage prevented: {reason}")
        print(f"💰 Saved: {tokens} tokens | {time_saved} min operator time | ${money_saved}\n")

# =====================================================================
# НОВЫЙ УЗЕЛ: DVP (Delta Verification Protocol)
# =====================================================================
class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold  # Порог допуска 5%

    def authorize_next_step(self, expected_value, actual_value, probe_type="FS_Probe"):
        """
        Анализирует физическую Дельту между обещанием ИИ и реальностью.
        Возвращает машиночитаемый статус для продолжения или разрыва цепи.
        """
        delta = actual_value - expected_value
        
        # 1. Агент соврал о выполнении (Ничего не сделано)
        if actual_value == 0 and expected_value > 0:
            return {
                "status": "HALT", 
                "color": "🔴",
                "reason": f"[{probe_type}] Zero Delta. Agent hallucinated execution."
            }
            
        # 2. Расчет допустимой погрешности (Tolerance)
        margin = expected_value * self.tolerance
        
        # 3. Агент перевыполнил задачу (Сбой цикла / Утечка ресурсов)
        if delta > margin:
            return {
                "status": "RECALIBRATE", 
                "color": "🟡",
                "reason": f"[{probe_type}] Delta exceeds +5% tolerance. Expected {expected_value}, got {actual_value}."
            }
            
        # 4. Агент не доделал задачу свыше допуска
        if delta < -margin:
            return {
                "status": "RECALIBRATE", 
                "color": "🟡",
                "reason": f"[{probe_type}] Delta falls below -5% tolerance. Expected {expected_value}, got {actual_value}."
            }
            
        # 5. Идеальное попадание или в пределах допуска 5%
        return {
            "status": "SYNCED", 
            "color": "🟢",
            "reason": f"[{probe_type}] Delta within tolerance. Integrity confirmed."
        }