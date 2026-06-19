import logging
import json
from .navigator import VikiNavigator

logger = logging.getLogger(__name__)

class VikiGraphController:
    def __init__(self, viki_core, db_path="viki_state.db"):
        self.viki = viki_core
        self.navigator = VikiNavigator(db_path)

    def execute_chain(self, task_id, steps_list, initial_state):
        saved = self.navigator.load_state(task_id)
        
        if saved:
            current_step_idx = saved["current_step"]
            state = saved["state_data"]
            last_status = saved["status"]
            
            # НОВОЕ: Профессиональное логирование возобновления
            if last_status == "PAUSE_FOR_SYNC":
                print(f"🔄 [CONDUCTOR] Resuming from PAUSE at step {current_step_idx}")
            else:
                print(f"🔄 [CONDUCTOR] Resuming Task {task_id} from Step {current_step_idx}")
        else:
            current_step_idx = 0
            state = initial_state
            last_status = "START"

        total = len(steps_list)

        for i in range(current_step_idx, total):
            current_task = steps_list[i]
            task_name = current_task.__name__.lower()

            if last_status == "PAUSE_FOR_SYNC" and i == current_step_idx:
                print(f"👤 [CONDUCTOR] Step {i} ({task_name}) AUTHORIZED BY HUMAN. Proceeding...")
                last_status = "ACTIVE"
            else:
                intent = {"action": task_name, "amount_usd": state.get("budget", 0)}
                auth = self.viki.authorize(intent)

                if auth["status"] == "FRICTION":
                    self.navigator.save_checkpoint(task_id, i, total, state, "PAUSE_FOR_SYNC")
                    print(f"⏸️ [CONDUCTOR] Step {i} ({task_name}) -> PAUSED. Awaiting Sync.")
                    return {"status": "PAUSED", "step": i}

                if auth["status"] == "BLOCKED":
                    self.navigator.save_checkpoint(task_id, i, total, state, "HALTED")
                    print(f"🛑 [CONDUCTOR] Step {i} ({task_name}) -> HALTED: {auth['reason']}")
                    return {"status": "HALTED", "reason": auth["reason"]}

            print(f"⚙️ [CONDUCTOR] Executing: {task_name}...")
            state = current_task(state)
            self.navigator.save_checkpoint(task_id, i + 1, total, state, "ACTIVE")
            
        print(f"🏁 [CONDUCTOR] Task {task_id} COMPLETED.")
        return {"status": "COMPLETED", "final_state": state}