import logging
from .navigator import VikiNavigator

logger = logging.getLogger(__name__)

class VikiGraphController:
    def __init__(self, viki_core, db_path="viki_state.db"):
        self.viki = viki_core
        self.navigator = VikiNavigator(db_path)

    def execute_chain(self, task_id, steps_list, initial_state):
        saved = self.navigator.load_state(task_id)
        current_step_idx = saved["current_step"] if saved else 0
        state = saved["state_data"] if saved else initial_state
        total = len(steps_list)

        for i in range(current_step_idx, total):
            current_task = steps_list[i]
            service_name = current_task.__name__

            # 1. Проверка Circuit Breaker
            if not self.viki.breaker.can_execute(service_name):
                return {"status": "HALTED", "reason": f"CIRCUIT_OPEN for {service_name}"}

            # 2. Sentinel Authorization
            intent = {"action": service_name, "amount_usd": state.get("budget", 0)}
            auth = self.viki.authorize(intent)

            # Трассировка в Черный Ящик
            self.navigator.log_trace(task_id, i, f"Executing {service_name}", auth["status"])

            if auth["status"] != "AUTHORIZED":
                self.navigator.save_checkpoint(task_id, i, total, state, auth["status"])
                return {"status": auth["status"], "step": i}

            # 3. Выполнение с обработкой ошибок для Breaker
            try:
                state = current_task(state)
                self.viki.breaker.report_success(service_name)
                self.navigator.save_checkpoint(task_id, i + 1, total, state, "ACTIVE")
            except Exception as e:
                self.viki.breaker.report_failure(service_name)
                self.navigator.save_checkpoint(task_id, i, total, state, "ERROR")
                return {"status": "ERROR", "reason": str(e)}
            
        return {"status": "COMPLETED", "final_state": state}