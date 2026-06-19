import sys
import os
import time
import uuid # Добавили импорт

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.parsers.anthropic_parser import AnthropicIntentParser
from viki.conductor import VikiGraphController

# 1. Инициализация (UUID гарантирует уникальность даже при 1000 запусках в сек)
task_id = f"RUN_{uuid.uuid4().hex[:8].upper()}"
parser = AnthropicIntentParser(api_key="STABLE_TEST")
viki = VIKI_Middleware(intent_parser=parser)
conductor = VikiGraphController(viki)

# 2. Шаги
def prepare(state): return state
def analyze(state): return state
def mass_mailing(state): return state 
def finalize(state): return state

my_steps = [prepare, analyze, mass_mailing, finalize]

print(f"\n>>> INITIATING DURABLE PIPELINE: {task_id}")

res = conductor.execute_chain(task_id, my_steps, {"budget": 100})

if res["status"] == "PAUSED":
    print("\n--- ⏸️ SYSTEM ON HOLD. HUMAN INTERVENTION SIMULATED ---")
    time.sleep(2)
    print("\n>>> RESUMING COMMAND ISSUED...")
    final_res = conductor.execute_chain(task_id, my_steps, {})
    
    if final_res["status"] == "COMPLETED":
        print("\n✅ SUCCESS: V.I.K.I. Sentinel maintained continuity and safety.")