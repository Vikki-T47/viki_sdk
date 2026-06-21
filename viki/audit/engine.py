# viki/audit/engine.py
from ..telemetry import VIKI_Telemetry

class PredictiveAudit:
    """Аудитор Плана. Проверяет всю цепочку ДО начала выполнения первого шага."""
    def __init__(self):
        self.telemetry = VIKI_Telemetry()

    def audit_chain_map(self, chain_map, enterprise_limits):
        total_planned_spend = sum(step.get('amount_usd', 0) for step in chain_map)
        max_limit = enterprise_limits.get('max_auto_transaction_usd', 1000)
        
        if total_planned_spend > max_limit:
            if hasattr(self.telemetry, 'log_predictive_block'):
                self.telemetry.log_predictive_block(total_planned_spend)
            return False, f"PREDICTIVE_HALT: Plan requires ${total_planned_spend}, limit is ${max_limit}."
            
        return True, "PLAN_AUTHORIZED"