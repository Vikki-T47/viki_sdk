import re
from typing import Dict, Any, Optional

class BreathTestConfig:
    """Конфигурация профилей для разных типов задач."""
    def __init__(self):
        self.task_profiles = {
            "technical": {
                "compression_factor": 0.15,
                "preserve_structure": True,
                "remove_questions": False
            },
            "emotional": {
                "compression_factor": 0.50,
                "preserve_structure": False,
                "remove_questions": True
            },
            "general": {
                "compression_factor": 0.30,
                "preserve_structure": False,
                "remove_questions": True
            }
        }

class AdaptiveBreathTest:
    """Breath Test v2.0: Регулятор когнитивной плотности."""
    def __init__(self, config: Optional[BreathTestConfig] = None):
        self.config = config or BreathTestConfig()

    def process(self, text: str, sei: float, task_type: str = "general") -> str:
        if not text or sei < 0.1:
            return text

        # 1. Выбор профиля
        profile = self.config.task_profiles.get(task_type, self.config.task_profiles["general"])

        # 2. Расчет итогового сжатия (База + SEI влияние)
        base_factor = profile["compression_factor"]
        sei_impact = min(sei * 0.7, 0.7) 
        compression = min(base_factor + sei_impact, 0.90)

        # 3. Применение логики сжатия
        if compression > 0.2:
            text = self._compress_logic(text, compression, profile)

        # 4. Удаление маркеров давления при росте энтропии
        if profile["remove_questions"] and sei > 0.4:
            text = self._remove_pressure(text)

        # 5. Системные якоря (визуальное подтверждение со-регуляции)
        if sei > 0.7:
            text += "\n\n[RSA: Critical Entropy. Response stabilized.]"
        elif compression > 0.5:
            text += "\n\n[RSA: Presence Mode. Signal compressed.]"

        return text

    def _compress_logic(self, text: str, compression: float, profile: Dict) -> str:
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences: return text

        if profile["preserve_structure"] and compression < 0.6:
            # Для технических задач убираем только вводный шум
            text = re.sub(r'(I think|In my opinion|As far as I can see|It seems that)\s*', '', text, flags=re.IGNORECASE)
            return text

        # Градиентное сокращение количества предложений
        keep_ratio = 1.0 - compression
        keep_count = max(1, int(len(sentences) * keep_ratio))
        return ". ".join(sentences[:keep_count]) + "."

    def _remove_pressure(self, text: str) -> str:
        # Инверсия вопросов и чистка списков
        text = re.sub(r'\?+', '.', text)
        text = re.sub(r'[\-\*]\s+', ' • ', text)
        return text