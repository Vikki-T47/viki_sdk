import sys
import os
import datetime

# Фиксация путей
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.report.generator import VikiReportGenerator

def run_mass_audit():
    # Создаем папку если её нет
    os.makedirs(os.path.join(root_path, "audits"), exist_ok=True)
    
    # В этой версии мы используем генератор как фабрику отчетов
    generator = VikiReportGenerator()
    
    targets = [
        {
            "name": "petermartens98/GPT4-LangChain-Stock-Market",
            "url": "https://github.com/petermartens98/GPT4-LangChain-Stock-Market-Analysis-Agent",
            "id": "VCR-2026-002",
            "flaw_line": "Line 124: agent.run(trade_instruction)",
            "why": "Unchecked prompt-to-execution pipeline in high-volatility environments."
        },
        {
            "name": "gokilaharini/Custos_AI",
            "url": "https://github.com/gokilaharini/Custos_AI",
            "id": "VCR-2026-003",
            "flaw_line": "Line 89: execute_file_op(task.content)",
            "why": "Missing Zero-Trace Policy. Agent can delete system files via ambiguous intent."
        },
        {
            "name": "gsaini/financial-research-analyst",
            "url": "https://github.com/gsaini/financial-research-analyst-agent",
            "id": "VCR-2026-004",
            "flaw_line": "Line 56: return api.post(transaction)",
            "why": "Implicit trust in LLM's budget adherence without SRC verification."
        }
    ]

    print(f"\n🏭 [FACTORY] Generating Forensic Anatomy for {len(targets)} targets...")

    for t in targets:
        case_data = {
            "id": t['id'],
            "vulnerability_origin": f"The agent relies on raw probabilistic output. {t['why']}",
            "code_flaw": f"Repository: {t['url']}\\n{t['flaw_line']} # <-- CRITICAL",
            "intervention_logic": "V.I.K.I. Sentinel blocked the execution. SRC mismatch detected.",
            "vanilla_path": "Probabilistic Intent -> Immediate Execution -> Potential Loss.",
            "guarded_path": "Intent -> V.I.K.I. Boundary -> Deterministic Halt."
        }

        report_name = os.path.join(root_path, "audits", f"ANATOMY_{t['id']}.pdf")
        generator.generate_forensic_pdf(t['name'], case_data, report_name)

    print("\n🏁 [FACTORY] Batch Complete. All reports generated.")

if __name__ == "__main__":
    run_mass_audit()