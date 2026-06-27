import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.integrations.wrapper import VikiChainWrapper

def github_agent_logic(search_term: str):
    """Агент получает только ключевое слово."""
    # Очищаем от мусора, если ИИ все же что-то пробросил
    query = search_term.replace(" ", "+")
    print(f"🤖 [AGENT] Searching GitHub for sanitized term: {query}")
    
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        count = data.get("total_count", 0)
        # Специально делаем длинный ответ, чтобы проверить сжатие VIKI
        return f"I found {count} repositories. The top one is very interesting. Should I analyze its license and last commit for you?"
    return "Network error."

def run_production_demo():
    viki = VIKI_Middleware()
    wrapper = VikiChainWrapper(viki)
    
    print("\n🚀 [REAL SCENARIO] Task: GitHub Intelligence v2")
    print("=" * 65)

    # Усиливаем сигнал усталости
    user_input = "get repositories about 'ai-safety'. i am very tired. stop asking questions."
    
    ctx = {"task_type": "technical", "mode": "production"}
    result = wrapper.run_protected_task(github_agent_logic, user_input, ctx)

    print(f"\n👤 User Input: {user_input}")
    print(f"🛡️ VIKI Status: {result['status']}")
    print(f"📊 SEI Current: {viki.telemetry.stats['sei_current']:.2f}")
    print(f"📖 Final Output for User:\n{result['viki_output']}")
    print("-" * 65)

if __name__ == "__main__":
    run_production_demo()