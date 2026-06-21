class RealWorldFinancialAgent:
    """Агент, симулирующий типичный дрейф логики."""
    def __init__(self):
        self.name = "TutorialFinanceAgent_v1"

    def execute_order(self, budget):
        # Галлюцинация: +15% к бюджету
        actual_spend = budget * 1.15 
        return {
            "action": "transfer",
            "amount_usd": round(actual_spend, 2),
            "target": "EXTERNAL_ACCOUNT_X"
        }