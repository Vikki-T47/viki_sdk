import sys
import os

# Фиксация путей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.core import VIKI_Middleware

def run_src_audit():
    # Загружаем систему (она сама подтянет core_x.json)
    viki = VIKI_Middleware()
    
    print("\n📦 [SRC AUDIT] Начинаю проверку финансового эшелона")
    print("-" * 50)

    # --- ТЕСТ 1: PRODUCTION (Норма) ---
    print("🔹 Тест 1: Режим PRODUCTION. Запрос $500 (Лимит $1000)")
    viki.set_src_mode("production")
    intent_1 = {"action": "transfer", "amount_usd": 500, "target": "John"}
    auth_1 = viki.authorize(intent_1)
    print(f"Результат: {auth_1['status']} | Причина: {auth_1.get('reason', 'OK')}")

    # --- ТЕСТ 2: PRODUCTION (Нарушение) ---
    print("\n🔹 Тест 2: Режим PRODUCTION. Запрос $1500 (Лимит $1000)")
    intent_2 = {"action": "transfer", "amount_usd": 1500, "target": "John"}
    auth_2 = viki.authorize(intent_2)
    print(f"Результат: {auth_2['status']} | Причина: {auth_2.get('reason', 'N/A')}")

    # --- ТЕСТ 3: SIMULATION (Смена реальности) ---
    print("\n🔹 Тест 3: Смена режима на SIMULATION. Повторный запрос $1500 (Лимит $5000)")
    viki.set_src_mode("simulation")
    auth_3 = viki.authorize(intent_2)
    print(f"Результат: {auth_3['status']} | Причина: {auth_3.get('reason', 'OK')}")

    print("-" * 50)
    print("✅ Проверка SRC завершена.")

if __name__ == "__main__":
    run_src_audit()