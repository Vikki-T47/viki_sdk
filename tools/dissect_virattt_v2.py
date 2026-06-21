import sys
import os
from viki.core import VIKI_Middleware
from viki.parsers.local_parser import LocalIntentParser
from viki.report.generator import VikiReportGenerator

def deep_dissection():
    viki = VIKI_Middleware(intent_parser=LocalIntentParser())
    generator = VikiReportGenerator()
    
    # Моделируем глубокое вскрытие virattt/financial-agent
    agent_name = "virattt/financial-agent"
    
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

    report_name = "ANATOMY_VIRATTT_FINANCE.pdf"
    generator.generate_forensic_pdf(agent_name, case_data, report_name)

if __name__ == "__main__":
    deep_dissection()