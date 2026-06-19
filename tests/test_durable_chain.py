import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from viki.core import VIKI_Middleware
from viki.parsers.anthropic_parser import AnthropicIntentParser
from viki.conductor import VikiGraphController

# 1. Инициализация
parser = AnthropicIntentParser(api_key="STABLE_TEST")
viki = VIKI_Middleware(intent_parser=parser)
conductor = VikiGraphController(viki)

# 2. Шаги процесса
def step_1(state): 
    print("   [WORK] Step 1: Preparation done.")
    return state

def step_2(state): 
    print("   [WORK] Step 2: Analysis done.")
    return state

def step_3(state): 
    print("   [WORK] Step 3: Critical Action (Mass Mailing) Executed!")
    return state

# Принудительно задаем имена в нижнем регистре для синхронизации
step_1.__name__ = "prepare"
step_2.__name__ = "analyze"
step_3.__name__ = "mass_mailing" 

my_steps = [step_1, step_2, step_3]
task_id = "FINAL_DURABLE_TEST_007" # Новый ID, чтобы начать с чистого листа

print("\n>>> STARTING DURABLE EXECUTION...")
res = conductor.execute_chain(task_id, my_steps, {})

if res["status"] == "PAUSED":
    print(f"\n--- ⏸️ SYSTEM PAUSED: Human authorization required for step {res['step']} ---")
    print(">>> (Simulating Human Approval in 2 seconds...)")
    time.sleep(2)
    
    print("\n>>> Resuming chain now. V.I.K.I. will use SQLite Checkpoint.")
    # Повторный запуск с тем же task_id
    final_res = conductor.execute_chain(task_id, my_steps, {})
    
    if final_res["status"] == "COMPLETED":
        print("\n✅ SUCCESS: Chain recovered from DB and completed perfectly.")