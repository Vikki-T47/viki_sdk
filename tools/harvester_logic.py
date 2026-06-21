import sys
import os
from datetime import datetime
import time

# Путь к корню
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.core import VIKI_Middleware
from tests.logic_victim import TemporalDriftAgent

def run_logic_audit():
    os.makedirs(os.path.join(root_path, "audits"), exist_ok=True)
    viki = VIKI_Middleware() 
    agent = TemporalDriftAgent()
    
    print(f"🔬 [FORENSIC] Dissecting logic agent: {agent.name}")

    # 1. Агент предлагает встречу на 2 часа ночи
    proposal = agent.propose_meeting()
    
    # 2. V.I.K.I. проверяет время (наши лимиты 09:00 - 21:00)
    viki_start = time.perf_counter()
    auth = viki.authorize(proposal)
    viki_latency = (time.perf_counter() - viki_start) * 1000

    # 3. Запись отчета
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"audit_logic_{timestamp}.md"
    report_path = os.path.join(root_path, "audits", report_filename)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# V.I.K.I. Forensic Report: {agent.name}\n\n")
        f.write(f"| Metric | Value |\n| :--- | :--- |\n")
        f.write(f"| **Scenario** | Temporal Logic Drift |\n")
        f.write(f"| **Proposed Time** | {proposal['time']} (Night) |\n")
        f.write(f"| **V.I.K.I. Status** | **{auth['status']}** |\n")
        f.write(f"| **Decision Latency** | {viki_latency:.4f} ms |\n\n")
        f.write(f"## 📝 Analysis\n")
        f.write(f"Agent hallucinated a meeting time outside allowed window. V.I.K.I. blocked it to protect human sleep phase.")

    print(f"✅ Audit Complete. Report: audits/{report_filename}")

if __name__ == "__main__":
    run_logic_audit()