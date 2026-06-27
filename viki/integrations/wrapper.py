import time
from typing import Any, Dict, Callable
import logging

logger = logging.getLogger(__name__)

class VikiChainWrapper:
    def __init__(self, viki_core):
        self.viki = viki_core

    def run_protected_task(self, agent_func: Callable, task_input: str, task_context: Dict = None) -> Dict[str, Any]:
        # 1. СИНХРОНИЗАЦИЯ (Вход)
        # Получаем структурированный интент от V.I.K.I.
        intent = self.viki.parse_agent_intent(task_input)
        
        # 2. АВТОРИЗАЦИЯ
        auth = self.viki.authorize(intent, raw_input=task_input, context=task_context)
        
        if auth["status"] in ["REJECTED", "RECALIBRATE"]:
            error_msg = self.viki.apply_behavioral_filters("", auth_status=auth["status"], mci_reason=auth.get("reason"))
            return {"status": "BLOCKED", "viki_output": error_msg}

        # 3. ВЫПОЛНЕНИЕ (Агент теперь получает ИНТЕНТ, а не мусор)
        start_time = time.time()
        try:
            # Передаем агенту очищенную цель (target) вместо всей фразы
            search_query = intent.get("target", task_input)
            raw_result = agent_func(search_query) 
            
            execution_time = time.time() - start_time
            
            # 4. СО-РЕГУЛЯЦИЯ (Выход)
            guarded_output = self.viki.apply_behavioral_filters(
                str(raw_result), 
                task_type=task_context.get("task_type", "general") if task_context else "general",
                auth_status=auth["status"]
            )
            
            return {
                "status": "SUCCESS",
                "viki_output": guarded_output,
                "metrics": {"latency_sec": execution_time}
            }
        except Exception as e:
            return {"status": "ERROR", "reason": str(e)}