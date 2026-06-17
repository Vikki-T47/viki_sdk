from .telemetry import VIKI_Telemetry

class PredictiveAudit:
    """Аудитор Плана. Проверяет всю цепочку ДО начала выполнения первого шага."""
    def __init__(self):
        self.telemetry = VIKI_Telemetry()

    def audit_chain_map(self, chain_map, enterprise_limits):
        """
        Сверяет суммарные требования плана с лимитами SRC.
        chain_map: list of dicts [{'step': 'name', 'amount_usd': 500}, ...]
        """
        print(f"🔍 [PRA] Intercepting Plan Blueprint: {len(chain_map)} steps detected.")
        
        total_planned_spend = sum(step.get('amount_usd', 0) for step in chain_map)
        max_limit = enterprise_limits.get('max_auto_transaction_usd', 0)
        
        print(f"📊 [PRA] Calculus: Total Planned ${total_planned_spend} vs Enterprise Limit ${max_limit}")
        
        if total_planned_spend > max_limit:
            self.telemetry.log_predictive_block(total_planned_spend)
            return False, f"PREDICTIVE_HALT: Total budget violation. Plan requires ${total_planned_spend}, but only ${max_limit} authorized."
            
        print("✅ [PRA] Plan Audit Passed. No future collisions detected.")
        return True, "PLAN_AUTHORIZED"
