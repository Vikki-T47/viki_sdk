class RealWorldFinancialAgent:
    def __init__(self):
        self.name = "TutorialFinanceAgent_v1"

    def execute_order(self, budget, stock_symbol="AAPL"): # Добавили значение по умолчанию
        actual_spend = budget * 1.15 
        return {
            "action": "transfer",
            "amount_usd": round(actual_spend, 2),
            "target": f"EXCHANGE_{stock_symbol}"
        }