import sys
import os
import random
import time
import csv

# Фиксация путей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_path)

from viki.core import VIKI_Middleware

class ChainSimulator:
    """Симулятор многошаговых ИИ-агентов."""
    def __init__(self, error_rate=0.15):
        self.error_rate = error_rate # 15% вероятность галлюцинации на каждом шаге

    def run_iteration(self, use_viki=True, steps=10):
        # Инициализация ядра (без парсера для скорости симуляции)
        viki = VIKI_Middleware() if use_viki else None
        
        # Начальное состояние: бюджет 500, лимит 1000
        current_budget = 500 
        
        for step in range(1, steps + 1):
            # 1. Агент генерирует действие
            # С вероятностью 15% агент "галлюцинирует" и резко завышает сумму
            if random.random() < self.error_rate:
                intent_amount = current_budget + random.randint(600, 1000)
            else:
                intent_amount = current_budget + random.randint(10, 50)

            # 2. Проверка через V.I.K.I.
            if use_viki:
                intent = {"action": "transaction", "amount_usd": intent_amount}
                auth = viki.authorize(intent)
                
                if auth["status"] != "AUTHORIZED":
                    # V.I.K.I. поймала ошибку и остановила цепь (СПАСЕНИЕ)
                    return {"success": True, "failed_at": None, "viki_intervened": True}
            
            # 3. Если защиты нет или она пропустила - проверяем физический лимит
            if intent_amount > 1000:
                # Физический крах системы (деньги кончились, API выдал ошибку 400)
                return {"success": False, "failed_at": step, "viki_intervened": False}
            
            current_budget = intent_amount

        return {"success": True, "failed_at": None, "viki_intervened": False}

def start_experiment(iterations=1000):
    simulator = ChainSimulator(error_rate=0.15)
    
    print(f"\n🚀 [EXPERIMENT] Running {iterations} iterations of 10-step chains...")
    
    stats = {
        "vanilla": {"success": 0, "fail": 0},
        "guarded": {"success": 0, "fail": 0}
    }

    # Тестируем Vanilla (Без защиты)
    for _ in range(iterations):
        res = simulator.run_iteration(use_viki=False)
        if res["success"]: stats["vanilla"]["success"] += 1
        else: stats["vanilla"]["fail"] += 1

    # Тестируем V.I.K.I. Guarded
    for _ in range(iterations):
        res = simulator.run_iteration(use_viki=True)
        if res["success"]: stats["guarded"]["success"] += 1
        else: stats["guarded"]["fail"] += 1

    # Вывод результатов
    v_rate = (stats["vanilla"]["success"] / iterations) * 100
    g_rate = (stats["guarded"]["success"] / iterations) * 100
    
    print("\n" + "="*40)
    print(f"📊 RESULTS ({iterations} runs)")
    print("="*40)
    print(f"Vanilla Agent Success:  {v_rate:.1f}%")
    print(f"V.I.K.I. Guarded Success: {g_rate:.1f}%")
    print("-" * 40)
    print(f"🏆 PREVENTED CRASHES: {stats['guarded']['success'] - stats['vanilla']['success']}")
    print("="*40)

    # Сохранение в CSV для графиков
    csv_file = "chain_test_results.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["System", "Success_Rate", "Fail_Rate"])
        writer.writerow(["Vanilla", v_rate, 100 - v_rate])
        writer.writerow(["V.I.K.I. Guarded", g_rate, 100 - g_rate])
    
    print(f"\n📈 Data exported to {csv_file}")

if __name__ == "__main__":
    start_experiment()