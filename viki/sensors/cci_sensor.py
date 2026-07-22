import re
from typing import List

class CCISensor:
    """
    Contextual Coherence Index (CCI) v1.0.
    Измеряет семантическую связность между текущим и прошлым вводом.
    """
    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold
        self.topic_history = []

    def calculate(self, text: str) -> float:
        # Упрощенный семантический анализ (поиск пересечений корней)
        words = set(re.findall(r'\w{4,}', text.lower()))
        
        if not self.topic_history:
            self.topic_history = words
            return 1.0 # Первая фраза — всегда эталон
        
        # Вычисляем коэффициент пересечения (Jaccard Index)
        intersection = words.intersection(self.topic_history)
        union = words.union(self.topic_history)
        
        cci = len(intersection) / len(union) if union else 0.0
        
        # Обновляем историю тем (с затуханием)
        self.topic_history = words 
        
        return round(cci, 2)