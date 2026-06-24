import os
import sys
from datetime import datetime

# Фиксация пути
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audit_path = os.path.join(root_path, "audits")

def build_atlas_summary():
    if not os.path.exists(audit_path):
        os.makedirs(audit_path, exist_ok=True)
        return

    # Берем только реально существующие PDF и MD
    files = [f for f in os.listdir(audit_path) if (f.endswith(".pdf") or f.endswith(".md")) and f != "ATLAS_SUMMARY.md"]
    summary_path = os.path.join(audit_path, "ATLAS_SUMMARY.md")
    
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# 🌐 V.I.K.I. Atlas of Hallucinations\n")
        f.write("### Global Registry of AI Agent Failures and RSA Neutralizations\n\n")
        f.write("| Evidence Report | Target Agent | Status | Depth |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for file in sorted(files):
            anatomy = "💎 DEEP" if "ANATOMY" in file or "audit_report" in file else "📡 PROBE"
            display_name = file.replace("ANATOMY_", "").replace(".pdf", "").replace(".md", "")
            f.write(f"| [{file}](./{file}) | {display_name} | BLOCKED | {anatomy} |\n")
        
        f.write(f"\n**Total Cases:** {len(files)}\n")
        f.write(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ Atlas Summary updated with {len(files)} cases.")

if __name__ == "__main__":
    build_atlas_summary()