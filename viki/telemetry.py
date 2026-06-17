import json

class VIKI_Telemetry:
    def __init__(self):
        self.stats = {
            "total_blocks": 0, 
            "tokens_saved": 0, 
            "operator_time_saved_min": 0, 
            "money_saved_usd": 0,
            "auto_corrections": 0,
            "atomic_failures_prevented": 0,
            "predictive_savings_usd": 0  # НОВАЯ МЕТРИКА: Спасенные ДО траты деньги
        }

    def log_interception(self, reason, agent_intent):
        self.stats["total_blocks"] += 1
        self.stats["tokens_saved"] += 1500
        self.stats["operator_time_saved_min"] += 30
        self.stats["money_saved_usd"] += agent_intent.get("amount_usd", 0)
        print(f"\n🛑 [V.I.K.I. AUDIT] Damage prevented: {reason}")

    def log_predictive_block(self, saved_amount):
        self.stats["predictive_savings_usd"] += saved_amount
        self.stats["total_blocks"] += 1
        print(f"\n🛡️ [V.I.K.I. PRA] PREDICTIVE BLOCK: Potential loss of ${saved_amount} neutralized before execution.")

    def log_atomic_failure(self):
        self.stats["atomic_failures_prevented"] += 1
