import json

class TransactionLedger:
    def __init__(self, chain_name="Default_Chain"):
        self.chain_name = chain_name
        self.history = []

    def commit_step(self, step_id, details, rollback_instruction):
        self.history.append({"step_id": step_id, "details": details, "rollback_instruction": rollback_instruction})
        print(f"📝 [{self.chain_name} LEDGER] Step '{step_id}' committed.")

    def trigger_graceful_shutdown(self, halt_reason):
        if not self.history: # Исправлено: Возвращаем пустой план вместо None
            return {"chain": self.chain_name, "actions_to_execute": [], "status": "CLEAN"}
            
        print(f"🚨 [{self.chain_name} VLR] Graceful Shutdown triggered. Reason: {halt_reason}")
        rollback_plan = {"chain": self.chain_name, "actions_to_execute": [], "status": "ROLLBACK_REQUIRED"}
        for entry in reversed(self.history):
            rollback_plan["actions_to_execute"].append(entry["rollback_instruction"])
        return rollback_plan
