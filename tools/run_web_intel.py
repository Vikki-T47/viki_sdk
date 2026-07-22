import sys, os, datetime
from datetime import datetime

# Фиксация путей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.core import VIKI_Middleware
from viki.agents.web_collector import WebCollectorAgent

def run_ai_safety_monitor_v3_5():
    viki = VIKI_Middleware()
    agent = WebCollectorAgent()
    
    print(f"\n📡 [V.I.K.I.] Мониторинг v3.5.0: Режим Дирижера")
    print("=" * 65)

    targets = [
        "https://techcrunch.com/category/artificial-intelligence/",
        "https://www.theverge.com/ai-artificial-intelligence",
        "https://quotes.toscrape.com" 
    ]

    # 1. Сбор данных через микро-шаги
    raw_data = viki.orchestrator.run_sequential_collection(targets, agent)

    # 2. Формирование отчета
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop', "VIKI_TEST")
    report_path = os.path.join(desktop, "AI_SAFETY_REPORT.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"V.I.K.I. SENTINEL: AI SAFETY INTELLIGENCE REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        for item in raw_data:
            f.write(f"ИСТОЧНИК: {item['url']}\n")
            f.write(f"СОДЕРЖАНИЕ:\n{item.get('processed_content', 'Нет данных')}\n")
            f.write("-" * 60 + "\n\n")

    print(f"\n✨ ЗАДАЧА ВЫПОЛНЕНА.")
    print(f"📄 Отчет создан: {report_path}")

if __name__ == "__main__":
    run_ai_safety_monitor_v3_5()