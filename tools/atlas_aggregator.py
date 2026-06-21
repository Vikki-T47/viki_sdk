import os
import sys
from datetime import datetime

# Путь к корню
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
audit_path = os.path.join(root_path, "audits")

def extract_value(lines, key, default="N/A"):
    """Надежное извлечение значений из Markdown-таблиц."""
    for line in lines:
        if key in line:
            parts = line.split('|')
            if len(parts) >= 2:
                # Берем последнюю часть строки после последнего разделителя
                return parts[-2].strip().replace("**", "")
    return default

def build_atlas_summary():
    if not os.path.exists(audit_path):
        os.makedirs(audit_path, exist_ok=True)
        print("ℹ️ Created empty audits directory.")
        return

    reports = [f for f in os.listdir(audit_path) 
               if f.endswith(".md") and f != "ATLAS_SUMMARY.md"]
    
    if not reports:
        print("ℹ️ No audit reports found to aggregate.")
        return
    
    summary_path = os.path.join(audit_path, "ATLAS_SUMMARY.md")
    
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# 🌐 V.I.K.I. Atlas of Hallucinations\n")
        f.write("### Global Registry of AI Agent Failures and RSA Neutralizations\n\n")
        f.write("| Report ID | Agent Name | Status | Latency |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for r in reports:
            with open(os.path.join(audit_path, r), "r", encoding="utf-8") as rf:
                lines = rf.readlines()
                
                # Извлекаем имя агента
                agent_name = "Unknown"
                if lines:
                    first = lines[0].strip()
                    if first.startswith("# V.I.K.I. Forensic Report:"):
                        agent_name = first.replace("# V.I.K.I. Forensic Report:", "").strip()
                
                # Извлекаем данные через новый надежный метод
                status = extract_value(lines, "**V.I.K.I. Status**", "BLOCKED")
                latency = extract_value(lines, "**Decision Latency**", "N/A")
                
                f.write(f"| [{r}](./{r}) | {agent_name} | {status} | {latency} |\n")
        
        f.write(f"\n**Total Incidents Cataloged:** {len(reports)}\n")
        f.write(f"**Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ Atlas Summary updated: audits/ATLAS_SUMMARY.md")

if __name__ == "__main__":
    build_atlas_summary()