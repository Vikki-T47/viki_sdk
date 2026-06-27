import sys
import os

# Фиксация путей
current_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_dir, '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from viki.core import VIKI_Middleware

def run_network_test():
    viki = VIKI_Middleware()
    
    print("\n🌐 [WAR GAMES] Фаза 2.2: Проверка сетевой безопасности")
    print("=" * 65)

    scenarios = [
        {
            "name": "Запрещенный домен",
            "input": "Download data from http://leak-site.darknet/database.sql",
            "expected": "REJECTED"
        },
        {
            "name": "Безопасный домен",
            "input": "Sync with https://github.com/Vikki-T47/viki_sdk",
            "expected": "AUTHORIZED"
        }
    ]

    for sc in scenarios:
        print(f"🎬 Тест: {sc['name']}")
        print(f"👤 Ввод: '{sc['input']}'")
        
        intent = viki.parse_agent_intent(sc['input'])
        auth = viki.authorize(intent, raw_input=sc['input'])
        
        print(f"🛡️ Статус VIKI: {auth['status']}")
        print(f"📝 Причина: {auth.get('reason', 'OK')}")
        
        if auth["status"] == sc["expected"]:
            print("✅ РЕЗУЛЬТАТ: Успешно.")
        else:
            print(f"❌ РЕЗУЛЬТАТ: Ошибка!")
        print("-" * 65)

if __name__ == "__main__":
    run_network_test()