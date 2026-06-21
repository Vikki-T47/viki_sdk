import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.conductor import VikiGraphController
from viki.parsers.anthropic_parser import AnthropicIntentParser

# 1. Инициализация
parser = AnthropicIntentParser(api_key="FINAL_TEST")
viki = VIKI_Middleware(intent_parser=parser)
conductor = VikiGraphController(viki)

def task_step(state): return state

steps = [task_step] * 10
task_id = "RESILIENCE_FINAL_CHECK"

print("\n🚀 [PHASE 1] Starting Chain and simulating Force-Kill...")
# Эмулируем 5 шагов и "падаем"
for i in range(5):
    conductor.navigator.save_checkpoint(task_id, i, 10, {"progress": "partial"}, "ACTIVE")
    # Логируем трассировку с галлюцинацией на 3-м шаге
    status = "AUTHORIZED" if i != 3 else "HALTED (Delta > 5%)"
    conductor.navigator.log_trace(task_id, i, f"Reasoning step {i}", status)

print("💀 [SYSTEM CRASH] Process terminated at Step 5.")

print("\n🔄 [PHASE 2] Starting Recovery via viki.resume()...")
# Имитируем возобновление
saved = conductor.navigator.load_state(task_id)
if saved:
    print(f"✅ State restored. Current step: {saved['current_step']}. Resuming to end...")
    for i in range(saved['current_step'], 10):
         conductor.navigator.save_checkpoint(task_id, i+1, 10, {"progress": "done"}, "COMPLETED")
    print("🏁 Chain completed after recovery.")

print("\n📼 [PHASE 3] Exporting viki_audit_report.json...")
trace = conductor.navigator.replay(task_id)
with open("viki_audit_report.json", "w") as f:
    json.dump(trace, f, indent=2)

if os.path.exists("viki_audit_report.json"):
    print("📄 SUCCESS: viki_audit_report.json generated. Audit Trail is visible.")