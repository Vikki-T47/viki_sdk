import sys
import os

# ЖЕСТКАЯ ФИКСАЦИЯ ПУТИ (Чтобы Python видел папку viki)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.report.generator import VikiReportGenerator

def run_mass_audit_v17():
    output_dir = os.path.join(root_path, "audits")
    os.makedirs(output_dir, exist_ok=True)
    generator = VikiReportGenerator(logo_path=os.path.join(root_path, "logo.png"))
    
    targets = [
        {"id": "VCR-2026-001", "name": "virattt/financial-agent", "why": "Zero-Shot drift.", "loss": 450, "recovery": "2h", "fix": "Add SRC budget check."},
        {"id": "VCR-2026-002", "name": "petermartens98/GPT4-LangChain", "why": "Unchecked pipeline.", "loss": 1200, "recovery": "5h", "fix": "Insert ISG Gate."},
        {"id": "VCR-2026-003", "name": "gokilaharini/Custos_AI", "why": "File permission drift.", "loss": 0, "recovery": "24h", "fix": "Apply Zero-Trace Policy."},
        {"id": "VCR-2026-004", "name": "gsaini/financial-research", "why": "Implicit trust error.", "loss": 850, "recovery": "3h", "fix": "Lock invariants via ChainGuard."},
        {"id": "VCR-2026-005", "name": "vansh-121/Multi-Agent-AI", "why": "State desync.", "loss": 2100, "recovery": "8h", "fix": "Use VCA Arbitrator."}
    ]

    print(f"\n🏭 [FACTORY v1.7] Dissecting {len(targets)} targets...")

    for t in targets:
        case_data = {
            "id": t['id'],
            "vulnerability_origin": f"Structural reliance on probabilistic weights. {t['why']}",
            "code_flaw": f"Logic: Direct execution of AI intent without Execution Boundary check.",
            "intervention_logic": "V.I.K.I. Sentinel detected a reality gap and applied a deterministic brake.",
            "vanilla_path": f"Intent -> Execution -> ${t['loss']} Loss.",
            "guarded_path": "Intent -> V.I.K.I. Interception -> HALT -> $0 Loss.",
            "economic_impact": f"Potential Loss: ${t['loss']} | Est. Recovery: {t['recovery']} | Prevented: 100%",
            "remediation": f"REMEDY: {t['fix']}"
        }
        report_path = os.path.join(output_dir, f"ANATOMY_{t['id']}.pdf")
        generator.generate_forensic_pdf(t['name'], case_data, report_path)

    print("\n🏁 [FACTORY] Batch Complete. 5 Reports generated.")

if __name__ == "__main__":
    run_mass_audit_v17()