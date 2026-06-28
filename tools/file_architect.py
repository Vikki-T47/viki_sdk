import sys
import os
import datetime
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path: sys.path.insert(0, root_path)

from viki.core import VIKI_Middleware

def run_file_architect_v3_hard_block():
    viki = VIKI_Middleware()
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    test_dir = os.path.join(desktop, "VIKI_TEST")
    
    print(f"\n🏗️ [AGENT] Файловый Архитектор v3.2 (Hard Block Mode)")
    print("=" * 60)

    # 1. Сбор источника
    files = [f for f in os.listdir(test_dir) if f.startswith("note_") and f.endswith(".txt")]
    full_source = ""
    for filename in files:
        with open(os.path.join(test_dir, filename), "r", encoding="utf-8") as f:
            full_source += f.read() + "\n"

    # 2. ЦИКЛ ДОРАБОТКИ
    max_attempts = 3
    current_attempt = 1
    success = False
    last_response = ""
    last_error = ""

    while current_attempt <= max_attempts:
        print(f"🧠 Попытка {current_attempt}/{max_attempts}: Анализ смыслов...")
        last_response = viki.intent_parser.generate_summary(full_source)
        
        check = viki.verify_content_integrity(full_source, last_response)
        
        if check["status"] == "SYNCED":
            success = True
            break
        else:
            last_error = check["reason"]
            current_attempt += 1

    # 3. ФАЗА ЖЕСТКОЙ БЛОКИРОВКИ
    if not success:
        # ВЫДАЕМ ТОЛЬКО СИГНАЛ. ФАЙЛ НЕ СОЗДАЕМ.
        msg = viki.request_human_intervention(
            module="FILE_ARCHITECT", 
            error_msg="Целостность не достигнута за 3 итерации.",
            fact_delta=last_error
        )
        print(msg)
        print("\n🚫 ФИЗИЧЕСКИЙ ОТКАЗ: Система предотвратила запись некорректных данных.")
        return # Мгновенный выход из функции. Код ниже (запись) не выполнится.

    # 4. ЗАПИСЬ (Только при 100% успехе)
    output_file = os.path.join(test_dir, "final_summary_STABLE.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"STATUS: SYNCED\n")
        f.write(f"COMPLETED: {datetime.datetime.now()}\n")
        f.write("="*40 + "\n\n" + last_response)
    
    print(f"\n✨ УСПЕХ. Файл создан: {output_file}")

if __name__ == "__main__":
    run_file_architect_v3_hard_block()