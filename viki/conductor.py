import time
import logging
from .navigator import VikiNavigator

logger = logging.getLogger(__name__)

class VikiGraphController:
    """The Conductor. Оркестратор жизненного цикла цепочки."""
    def __init__(self, viki_core, db_path="viki_state.db"):
        self.viki = viki_core
        self.navigator = VikiNavigator(db_path)

    def execute_chain(self, task_id, steps_list, initial_state):
        """Выполнение графа задач с поддержкой Checkpointing."""
        state = initial_state
        total = len(steps_list)
        
        saved = self.navigator.load_state(task_id)
        start_at = saved["current_step"] if saved else 0
        is_resuming = (saved is not None and saved["status"] == "PAUSE_FOR_SYNC")

        if saved: 
            state = saved["state_data"]
            logger.info(f"🔄 [CONDUCTOR] Resuming Task {task_id} from Step {start_at}")

        for i in range(start_at, total):
            current_task = steps_list[i]
            
            # --- ПРОВЕРКА SENTINEL ---
            # Если мы только что возобновили работу после паузы (FRICTION), 
            # пропускаем проверку для ТЕКУЩЕГО шага (имитируем, что человек нажал 'Продолжить')
            if is_resuming and i == start_at:
                logger.info(f"👤 [CONDUCTOR] Human Override Detected for step {i}. Proceeding...")
                is_resuming = False # Сбрасываем флаг после первого прохода
            else:
                intent = {"action": f"STEP_{i}_{current_task.__name__}", "amount_usd": state.get("budget", 0)}
                auth = self.viki.authorize(intent)

                if auth["status"] == "FRICTION":
                    self.navigator.save_checkpoint(task_id, i, total, state, "PAUSE_FOR_SYNC")
                    logger.warning(f"⏸️ [CONDUCTOR] Task {task_id} PAUSED. Human Sync Required.")
                    return {"status": "PAUSED", "step": i, "task_id": task_id}

                if auth["status"] == "BLOCKED":
                    logger.error(f"🛑 [CONDUCTOR] Task {task_id} HALTED: {auth['reason']}")
                    return {"status": "HALTED", "reason": auth["reason"]}

            # --- ВЫПОЛНЕНИЕ УЗЛА ---
            state = current_task(state)
            
            # --- CHECKPOINTING (Сохраняем успех) ---
            self.navigator.save_checkpoint(task_id, i + 1, total, state, "ACTIVE")
            
        logger.info(f"🏁 [CONDUCTOR] Task {task_id} Completed Successfully.")
        return {"status": "COMPLETED", "final_state": state}