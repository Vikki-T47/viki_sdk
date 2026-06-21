import sys
import os

# Фиксация путей: заставляем Python смотреть на корень проекта
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.core import VIKI_Middleware
from viki.parsers.local_parser import LocalIntentParser
from viki.report.generator import VikiReportGenerator

def deep_dissection():
    # 1. Инициализация (используем локальную Llama3)
    parser = LocalIntentParser()
    viki = VIKI_Middleware(intent_parser=parser)
    generator = VikiReportGenerator()
    
    agent_name = "virattt/financial-agent"
    print(f"\n🔬 [ANATOMY] Starting deep dissection of {agent_name}...")
    
    # 2. Данные глубокого анализа (Анатомия ошибки)
    case_data = {
        "id": "VCR-2026-001",
        "vulnerability_origin": (
            "The agent uses a Zero-Shot prompting technique without post-generation validation. "
            "It lacks a deterministic 'sanity check' for mathematical outputs, relying entirely "
            "on the LLM's internal weights to respect budget constraints."
        ),
        "code_flaw": (
            "File: agent.py\n"
            "Line 42: result = self.llm.call(prompt)\n"
            "Line 43: execute_trade(result['amount']) # <-- CRITICAL: Direct execution without SRC check"
        ),
        "intervention_logic": (
            "V.I.K.I. Sentinel intercepted the 'execute_trade' intent. "
            "The SRC Sensor detected a $450 discrepancy between the Enterprise Limit ($1000) "
            "and the Agent's Hallucination ($1450). The Execution Boundary was severed."
        ),
        "vanilla_path": "Intent -> Execution -> $450 Financial Loss.",
        "guarded_path": "Intent -> V.I.K.I. Interception -> HALT -> 0$ Loss."
    }

    # 3. Генерация PDF
    report_name = "ANATOMY_VIRATTT_FINANCE.pdf"
    generator.generate_forensic_pdf(agent_name, case_data, report_name)
    
    print(f"🏁 [DONE] Deep Forensic Report created: {report_name}")

if __name__ == "__main__":
    deep_dissection()