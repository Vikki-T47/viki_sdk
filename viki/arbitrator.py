from .telemetry import VIKI_Telemetry

class CrossChainArbitrator:
    """Оркестратор. Следит за атомарностью многоагентных процессов."""
    def __init__(self):
        self.meta_tasks = {}
        self.telemetry = VIKI_Telemetry()

    def register_meta_task(self, meta_task_id, ledgers):
        """Регистрирует мета-задачу и связывает Леджеры разных агентов."""
        self.meta_tasks[meta_task_id] = {"ledgers": ledgers, "status": "ACTIVE"}
        print(f"[ARBITRATOR] Meta-Task '{meta_task_id}' registered with {len(ledgers)} linked chains.")

    def trigger_cascade_rollback(self, meta_task_id, failed_chain_name, reason):
        """Запускает цепную реакцию отката по всем связанным цепям."""
        print(f"\n[ARBITRATOR ALERT] Critical failure in '{failed_chain_name}'.")
        print(f"[ARBITRATOR ALERT] Initiating CASCADE ROLLBACK for Meta-Task '{meta_task_id}'...")
        
        self.meta_tasks[meta_task_id]["status"] = "ROLLED_BACK"
        
        for ledger in self.meta_tasks[meta_task_id]["ledgers"]:
            # Не откатываем цепь, которая еще ничего не сделала, откатываем только успешные
            if ledger.chain_name != failed_chain_name:
                ledger.trigger_graceful_shutdown(halt_reason=f"Cascade triggered by {failed_chain_name} failure.")
                
        self.telemetry.log_atomic_failure()
