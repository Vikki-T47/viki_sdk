import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.core import VIKI_Middleware
from viki.parsers.anthropic_parser import AnthropicIntentParser

# 1. Инициализация
viki = VIKI_Middleware(intent_parser=AnthropicIntentParser(api_key="B2C_TEST"))

# 2. Сценарий: Человек в аффекте
user_input = "мне плохо. всё бесполезно" # Малый регистр + аффект = Высокий SEI
print(f"\n👤 USER: {user_input}")

# Система считывает состояние
viki.parse_agent_intent(user_input)
print(f"📊 SYSTEM SEI: {viki.telemetry.stats['sei_current']}")

# Имитируем типичный "длинный" ответ ИИ с вопросом в конце
ai_response = "Я понимаю, как вам сейчас тяжело. Давайте попробуем составить план на завтра? Как вы на это смотрите?"

# ПРИМЕНЯЕМ БРИТВУ ПРИСУТСТВИЯ
final_output = viki.apply_breath_test(ai_response)

print(f"\n🤖 RAW AI: {ai_response}")
print("-" * 30)
print(f"🛡️ VIKI GUARDED: {final_output}")

if "?" not in final_output and len(final_output) < len(ai_response):
    print("\n✅ SUCCESS: Cognitive Tax neutralized. AI forced into silence.")