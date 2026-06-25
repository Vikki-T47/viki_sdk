import logging
from .navigator import VikiNavigator

logger = logging.getLogger(__name__)

class VikiGraphController:
    def __init__(self, viki_core, db_path="viki_state.db"):
        self.viki = viki_core
        self.navigator = VikiNavigator(db_path)

    def execute_chain(self, task_id, steps_list, initial_state):
        # 1. ЗАМОРОЗКА ИНВАРИАНТОВ
        self.viki.lock_chain_invariants({
            "base_price": initial_state.get("base_price", 0),
            "currency": initial_state.get("currency", "USD")
        })

        current_state = initial_state
        total = len(steps_list)

        for i, step in enumerate(steps_list):
            agent_id = f"Agent_Step_{i}"
            try:
                # Агент выполняет шаг
                new_state = step(current_state)
                
                # 2. ПРОВЕРКА CHAIN GUARD (Стык между агентами)
                validation = self.viki.verify_cascade(new_state, agent_id)
                
                if validation["status"] == "VIOLATION":
                    print(f"🛑 [CONDUCTOR] Cascade breach at {agent_id}: {validation['reason']}")
                    return {"status": "HALTED", "reason": validation["reason"]}

                current_state = new_state
                self.navigator.save_checkpoint(task_id, i + 1, total, current_state, "ACTIVE")
                
            except Exception as e:
                return {"status": "ERROR", "reason": str(e)}

        return {"status": "COMPLETED", "final_state": current_state}