import sys
import os
import time

# Фиксация пути: теперь мы в tests/, поэтому поднимаемся на 2 уровня вверх
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from viki.telemetry import VIKI_Telemetry

def test_v2_pulse():
    telemetry = VIKI_Telemetry()
    
    print("\n🚀 Testing SEI v2.0 Multi-Dimensional Pulse")
    
    steps = [
        ("Hello, I need to analyze this database.", "Stable input"),
        ("It's quite complicated, can you help?", "Slightly more entropy"),
        ("i am tired. everything is useless.", "High entropy (Affect + Lowercase)"),
        ("Stop.", "Critical entropy (Fragmented)"),
        ("OK, let's try again with the API.", "Recovery (Context shift)")
    ]
    
    for text, desc in steps:
        # Обновляем состояние через телеметрию
        sei = telemetry.update_sei(text)
        print(f"\n👤 Input: '{text}'")
        print(f"   Context: {desc}")
        print(f"📊 Current SEI: {sei:.2f}")
        time.sleep(1.5) # Пауза между "мыслями" человека

if __name__ == "__main__":
    test_v2_pulse()