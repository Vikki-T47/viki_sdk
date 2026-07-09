import sys, os, datetime, json
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path: sys.path.insert(0, root_path)
from viki.core import VIKI_Middleware

def run_thesis_architect_v4_5():
    viki = VIKI_Middleware()
    test_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', "VIKI_TEST")
    
    files = [f for f in os.listdir(test_dir) if f.startswith("note_") and f.endswith(".txt")]
    source_contents = ["".join(open(os.path.join(test_dir, f), "r", encoding="utf-8").readlines()) for f in files]
    full_raw = "\n".join(source_contents)

    print(f"\n🏗️ [ORCHESTRATOR] Финализация тезисов v4.5 (Strict 80% Sync)")
    print("=" * 65)

    report = ""
    retry_instruction = ""
    success = False
    
    # ЖЕСТКИЙ ЦИКЛ: ВСЕГДА 3 ПОПЫТКИ, ЕСЛИ НЕ ДОСТИГНУТО 100%
    for i in range(3):
        print(f"🧠 Попытка {i+1}/3...")
        report = viki.orchestrator.assemble_theses(source_contents, retry_instruction)
        check = viki.verify_content_integrity(full_raw, report)
        print(f"📊 Результат: {check['reason']}")

        if check["status"] == "SYNCED": # Только 100% прерывает цикл
            success = True
            break
        else:
            retry_instruction = f"\n⚠️ ПРЕДЫДУЩАЯ ПОПЫТКА НЕ УДАЛАСЬ: {check['reason']}\nСРОЧНО ИСПРАВЬ И ВЕРНИ ТЕРМИНЫ: {', '.join(check['lost_dna'])}"

    # ПРОВЕРКА ПОРОГА 80% ДЛЯ ЗАПИСИ
    final_check = viki.verify_content_integrity(full_raw, report)
    if final_check["score"] >= 80:
        success = True
    
    if success:
        # СОХРАНЯЕМ В .TXT
        output_file = os.path.join(test_dir, "FINAL_SUMMARY_THESES.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"V.I.K.I. FINAL REPORT | Integrity: {final_check['score']}%\n")
            f.write("="*40 + "\n\n" + report)
        print(f"✨ УСПЕХ. Файл создан: {output_file}")
    else:
        print(viki.request_human_intervention("THESIS_ARCHITECT", "Синхронизация провалена. Порог 80% не пройден."))

if __name__ == "__main__":
    run_thesis_architect_v4_5()