import json

class TransactionLedger:
    def __init__(self):
        self.history = []

    def commit_step(self, step_id, details, rollback_instruction):
        """Записывает успешный шаг и инструкцию по его отмене."""
        self.history.append({
            "step_id": step_id,
            "details": details,
            "rollback_instruction": rollback_instruction
        })
        print(f"📝 [LEDGER] Step '{step_id}' committed. Rollback protocol saved.")

    def trigger_graceful_shutdown(self, halt_reason):
        """Генерирует машиночитаемый JSON для отката системы (LIFO)."""
        print(f"\n🚨 [VLR PROTOCOL INITIATED] Graceful Shutdown triggered.")
        
        rollback_plan = {
            "status": "ROLLBACK_REQUIRED",
            "reason": halt_reason,
            "actions_to_execute": []
        }
        
        # Откат идет в обратном порядке (от последнего шага к первому)
        for entry in reversed(self.history):
            rollback_plan["actions_to_execute"].append(entry["rollback_instruction"])
        
        print(">>> EXTERNAL API ROLLBACK INSTRUCTIONS GENERATED <<<")
        print(json.dumps(rollback_plan, indent=2))
        
        return rollback_plan
