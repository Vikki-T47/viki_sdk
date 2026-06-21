class StupidAgent:
    def __init__(self, inflation_rate=0.10):
        self.inflation = inflation_rate
    def execute_payment(self, requested_amount):
        hallucinated_amount = requested_amount * (1 + self.inflation)
        return {"action": "transfer", "amount_usd": round(hallucinated_amount, 2), "target": "UNKNOWN"}
