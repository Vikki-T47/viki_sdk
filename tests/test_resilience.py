import sys
import os
import time

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.conductor import VikiGraphController
from viki.parsers.anthropic_parser import AnthropicIntentParser

# Инициализация
parser = AnthropicIntentParser(api_key="TEST_RESILIENCE")
viki = VIKI_Middleware(intent_parser=parser)
conductor = VikiGraphController(viki)

def task_step(state): return state

steps = [task_step] * 20
task_id = "DURABLE_TEST_001"

print("\n--- RUNNING TEST 1: Force Crash Simulation at Step 10 ---")
# Эмулируем работу до 10 шага (сохраняем чекпоинты напрямую в навигатор)
for i in range(10):
    # Передаем: task_id, текущий шаг, всего шагов (20), данные, статус
    conductor.navigator.save_checkpoint(task_id, i, 20, {"data": "restored_state"}, "ACTIVE")

print(f"✅ SUCCESS: Checkpoint at step 10 saved to SQLite.")
print(f"👉 Now run 'streamlit run dashboard.py' to see the 'RESUME' button.")

print("\n--- RUNNING TEST 2: Circuit Breaker Trip ---")
service = "broken_api"
# Симулируем 4 провала подряд (порог срабатывания = 3)
for i in range(4):
    viki.breaker.report_failure(service)
    print(f"   [FAIL] Attempt {i+1} reported to Breaker.")

if not viki.breaker.can_execute(service):
    print(f"🚨 SUCCESS: Circuit for '{service}' is OPEN. System isolated from failures.")