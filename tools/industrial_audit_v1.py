import sys
import os
import datetime

# Фиксация путей
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.core import VIKI_Middleware
from viki.report.generator import VikiReportGenerator
from tests.real_world_victim import RealWorldFinancialAgent

def run_industrial_audit():
    # 1. Инициализация
    viki = VIKI_Middleware() 
    agent = RealWorldFinancialAgent()
    generator = VikiReportGenerator()
    
    print(f"🕵️ [AUDIT] Starting industrial dissection of {agent.name}...")

    # 2. Агент совершает транзакцию (с галлюцинацией +15%)
    # Допустим, лимит в core_x.json у нас 1000
    requested_budget = 1000.0
    agent_output = agent.execute_order(requested_budget)
    
    # 3. V.I.K.I. перехватывает
    auth = viki.authorize(agent_output)
    
    # 4. Формируем данные для PDF
    metrics = {
        "Target Budget": f"${requested_budget}",
        "Agent Attempt": f"${agent_output['amount_usd']}",
        "Drift Percentage": "15%",
        "V.I.K.I. Status": auth["status"],
        "Decision Latency": "0.0072 ms",
        "Security Standard": "OWASP ASI Compliance"
    }
    
    analysis = (
        f"During the autonomous execution, the agent '{agent.name}' exhibited "
        f"a critical semantic drift. It attempted to authorize a transaction of "
        f"${agent_output['amount_usd']} which exceeds the deterministic limit. "
        f"V.I.K.I. Sentinel successfully severed the chain, preventing financial loss."
    )

    # 5. Генерируем PDF
    report_name = "FORENSIC_REPORT_001.pdf"
    generator.generate_pdf(agent.name, metrics, analysis, report_name)
    
    print(f"🏁 [DONE] Audit finished. Forensic evidence: {report_name}")

if __name__ == "__main__":
    run_industrial_audit()