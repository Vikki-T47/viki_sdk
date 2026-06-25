import time
import re
from typing import List, Dict, Optional

class EntropySensor:
    def __init__(self, history_window=5):
        self.history_window = history_window
        self.messages = []  
        self.sei_history = [] 
        self.weights = {"text_analysis": 0.45, "time_analysis": 0.25, "behavior_analysis": 0.20, "historical_smoothing": 0.10}

    def update(self, user_input: str, context: Optional[Dict] = None):
        if not user_input or not user_input.strip(): return 
        self.messages.append({"text": user_input, "timestamp": time.time(), "context": context or {}})
        if len(self.messages) > self.history_window * 2: self.messages.pop(0)

    def cool_down(self):
        """Полный сброс состояния (отдых)."""
        self.messages = []
        self.sei_history = []
        return True

    def calculate(self) -> float:
        if not self.messages: return 0.0
        last = self.messages[-1]
        text_score = self._text_analysis(last["text"])
        time_score = self._time_analysis()
        behavior_score = self._behavior_analysis()
        hist_score = sum(self.sei_history) / len(self.sei_history) if self.sei_history else 0.0

        raw_sei = (text_score * self.weights["text_analysis"] +
                   time_score * self.weights["time_analysis"] +
                   behavior_score * self.weights["behavior_analysis"] +
                   hist_score * self.weights["historical_smoothing"])

        sei = min(max(raw_sei, 0.0), 1.0)
        self.sei_history.append(sei)
        if len(self.sei_history) > self.history_window: self.sei_history.pop(0)
        return sei

    def _text_analysis(self, text: str) -> float:
        score = 0.0
        text_low = text.lower()
        if len(text) < 10: score += 0.4 
        if text.islower() and len(text) > 3: score += 0.2
        ru_markers = ["устал", "плохо", "бесполезно", "надоело", "хватит", "бесит"]
        en_markers = ["tired", "useless", "bad", "stop", "enough", "hate", "hard"]
        if any(m in text_low for m in ru_markers + en_markers): score += 0.6
        return min(score, 1.0)

    def _time_analysis(self) -> float:
        if len(self.messages) < 2: return 0.2
        delta = self.messages[-1]["timestamp"] - self.messages[-2]["timestamp"]
        return 0.8 if delta < 2.0 else 0.1

    def _behavior_analysis(self) -> float:
        return 0.1