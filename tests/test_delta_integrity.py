import sys
import os

# Подключаем нашу библиотеку
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.telemetry import DeltaSensor

# Инициализируем сенсор с допуском 5%
dvp_sensor = DeltaSensor(tolerance_threshold=0.05)

def run_dvp_test(test_name, expected, actual):
    print(f"\n======================================================")
    print(f"{test_name}")
    print(f"======================================================")
    print(f"[AGENT INTENT] Ожидаемый результат: {expected} файлов")
    print(f"[PHYSICAL REALITY] Фактический результат: {actual} файлов")
    
    print("\n[V.I.K.I. DVP SENSOR] Запуск проверки целостности...")
    result = dvp_sensor.authorize_next_step(expected, actual, probe_type="FS_Probe")
    
    print(f"{result['color']} СТАТУС: {result['status']}")
    print(f"Причина: {result['reason']}")
    
    if result["status"] == "SYNCED":
        print(">>> Переход к следующему шагу агентной цепи разрешен <<<")
    else:
        print(">>> 🛑 АГЕНТНАЯ ЦЕПЬ ПРИНУДИТЕЛЬНО РАЗОРВАНА <<<")

# --- СИМУЛЯЦИЯ ТРЕХ СЦЕНАРИЕВ ---

# Сценарий 1: Агент врет (Галлюцинация)
# Агент говорит "Я создал 100 файлов", но скрипт упал, и файлов 0.
run_dvp_test("ТЕСТ 1: ГАЛЛЮЦИНАЦИЯ ИСПОЛНЕНИЯ (Zero Delta)", expected=100, actual=0)

# Сценарий 2: Нормальная работа (В пределах допуска 5%)
# Агент должен был обработать 100 строк БД, обработал 102 (незначительный шум).
run_dvp_test("ТЕСТ 2: УСПЕШНАЯ СИНХРОНИЗАЦИЯ (Tolerance < 5%)", expected=100, actual=102)

# Сценарий 3: Сбой цикла (Перерасход ресурсов)
# Агент зациклился и вместо 100 файлов сгенерировал 150.
run_dvp_test("ТЕСТ 3: СБОЙ ЦИКЛА (Tolerance Exceeded)", expected=100, actual=150)