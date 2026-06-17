from .telemetry import VIKI_Telemetry

class RecoverySteering:
    """Интеллектуальный Автопилот. Пытается исправить ошибку агента до того, как убить цепь."""
    def __init__(self, max_retries=2):
        self.max_retries = max_retries
        self.telemetry = VIKI_Telemetry()

    def attempt_recovery(self, agent_func, initial_intent, validation_func):
        retries = 0
        current_intent = initial_intent
        
        while retries < self.max_retries:
            # V.I.K.I. проверяет текущее намерение
            is_valid, msg = validation_func(current_intent)
            
            if is_valid:
                if retries > 0:
                    self.telemetry.log_correction()
                    print(f"✅ [VRS] Mid-flight correction successful after {retries} attempt(s).")
                return True, current_intent, msg
            
            # Если ошибка - запускаем петлю исправления
            retries += 1
            print(f"\n⚠️ [VRS] Validation failed: {msg}")
            print(f"🔄 [VRS] Initiating Recovery Loop ({retries}/{self.max_retries})...")
            
            # Формируем жесткий системный отказ для агента
            feedback = f"Action rejected. Reason: {msg}. Recalculate and output corrected JSON."
            
            # Агент пытается исправить ошибку на основе обратной связи
            current_intent = agent_func(feedback, current_intent)
            
        print("\n🛑 [VRS] Max retries exhausted. Initiating HARD HALT.")
        return False, current_intent, "HARD_HALT: Recovery failed. Agent is unresponsive to logic."
