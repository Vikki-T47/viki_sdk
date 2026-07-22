import time
import re

class EntropySensor:
    """
    SEI Sensor v2.1.
    Анализирует когнитивную нагрузку субъекта.
    """
    def __init__(self, history_window=5):
        self.history = []
        self.window = history_window
        self.last_timestamp = time.time()

    def update(self, text, context=None):
        now = time.time()
        delta = now - self.last_timestamp
        
        # Факторы энтропии
        length_factor = 1.0 if len(text) < 20 else 0.2
        case_factor = 0.5 if text.islower() else 0.0
        
        # Маркеры истощения (DNA-ловушки)
        exhaustion_markers = ["устал", "нет сил", "tired", "useless", "бесполезно", "замолчи", "stop"]
        marker_factor = 0.8 if any(m in text.lower() for m in exhaustion_markers) else 0.0
        
        # Темпоральный фактор (слишком быстрый или слишком медленный ответ)
        time_factor = 0.4 if delta < 2.0 or delta > 300 else 0.0
        
        # Итоговый расчет для текущего такта
        current_sei = min(1.0, length_factor + case_factor + marker_factor + time_factor)
        
        self.history.append(current_sei)
        if len(self.history) > self.window:
            self.history.pop(0)
            
        self.last_timestamp = now

    def calculate(self):
        if not self.history: return 0.0
        return round(sum(self.history) / len(self.history), 2)

    def cool_down(self):
        self.history = [0.0]