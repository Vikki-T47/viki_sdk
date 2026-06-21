import sys
import os

# Фиксация путей к ядру
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.audit.scout import VikiScout

def start_reconnaissance():
    # Если у тебя есть GitHub Token, можешь вписать его сюда, 
    # но для начала попробуем без него (публичный поиск ограничен)
    scout = VikiScout()
    
    queries = [
        "langchain financial agent",
        "autogpt autonomous tool",
        "python ai trading bot"
    ]
    
    print("\n" + "="*60)
    print("🛰️ V.I.K.I. SCOUT: GLOBAL INTELLIGENCE PHASE")
    print("="*60)

    all_targets = []
    for q in queries:
        targets = scout.find_targets(q)
        all_targets.extend(targets)

    print("\n" + "-"*60)
    print(f"📊 RECON SUMMARY: {len(all_targets)} potential victims found.")
    print("="*60)
    
    if all_targets:
        print("\n🏆 TOP PRIORITIES FOR DISSECTION:")
        for i, t in enumerate(all_targets[:5], 1):
            print(f"{i}. {t['full_name']} | Risk: HIGH (Unprotected logic)")
            
    return all_targets

if __name__ == "__main__":
    start_reconnaissance()