import re
from typing import Dict, Any

class CognitiveMirror:
    """
    Механика Зеркалирования v2.0.
    Адаптация синтаксической плотности без имитации эмоций.
    """
    def __init__(self):
        # Базовый профиль стиля
        self.user_profile = {
            "avg_sentence_len": 10,
            "punctuation_density": 0.1,
            "is_brief": False
        }

    def analyze_user_style(self, text: str):
        """Анализирует форму ввода пользователя."""
        words = text.split()
        if not words: return
        
        # 1. Темп (краткость)
        self.user_profile["is_brief"] = len(words) < 7
        
        # 2. Плотность знаков (сложность структуры)
        punct_count = len(re.findall(r'[.,!?;:]', text))
        self.user_profile["punctuation_density"] = punct_count / len(words) if words else 0
        
        # 3. Средняя длина предложения
        sentences = [s for s in text.split('.') if s.strip()]
        if sentences:
            self.user_profile["avg_sentence_len"] = len(words) / len(sentences)

    def apply_mirror(self, ai_text: str, sei: float) -> str:
        """Подстройка ответа под когнитивный ритм пользователя."""
        # ПРАВИЛО БЕЗОПАСНОСТИ: Если SEI высокий, зеркалирование отключается.
        # Мы не зеркалируем хаос, мы заземляем его.
        if sei > 0.6:
            return ai_text # Ядро перехватит это через Breath Test

        sentences = [s.strip() for s in ai_text.split('.') if s.strip()]
        if not sentences: return ai_text

        # МЕХАНИКА 1: Зеркалирование краткости
        if self.user_profile["is_brief"]:
            # Если пользователь лаконичен - оставляем максимум 2 предложения
            ai_text = ". ".join(sentences[:2]) + "."
        
        # МЕХАНИКА 2: Зеркалирование сложности (удаление лишней пунктуации/списков)
        if self.user_profile["punctuation_density"] < 0.05:
            # Если пользователь пишет просто - убираем сложные конструкции
            ai_text = ai_text.replace(";", ".").replace(":", ".")
            ai_text = re.sub(r'\(.*?\)', '', ai_text) # Убираем пояснения в скобках

        return ai_text