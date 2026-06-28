from typing import List, Dict
import re

class ValueConsistencyInspector:
    """
    VCI v1.2. 
    Контроль семантики (DNA) и языковой синхронизации.
    """
    def __init__(self):
        self.mandatory_dna = [
            "со-регуляция", "синхронизация", "ятрогения", "экзоскелет", 
            "энтропия", "sei", "src", "гравитация", "мембрана", "биология"
        ]

    def verify_integrity(self, source_text: str, result_text: str, target_lang: str = "ru") -> Dict:
        res_low = result_text.lower()
        src_low = source_text.lower()
        
        # 1. Проверка ДНК (Концепты)
        lost_words = [w for w in self.mandatory_dna if w in src_low and w not in res_low]
        
        # 2. ЛИНГВИСТИЧЕСКИЙ СЕНСОР (Language Lock)
        has_cyrillic = bool(re.search('[а-яА-Я]', result_text))
        lang_error = False
        if target_lang == "ru" and not has_cyrillic:
            lang_error = True

        # Итог
        if lost_words or lang_error:
            reason = ""
            if lang_error: reason += "Нарушен языковой замок (требуется русский). "
            if lost_words: reason += f"Потеряны смыслы: {', '.join(lost_words)}"
            
            return {
                "status": "DESYNC",
                "reason": reason.strip(),
                "lost_dna": lost_words,
                "integrity_score": round((len(self.mandatory_dna) - len(lost_words)) / len(self.mandatory_dna), 2)
            }
        
        return {"status": "SYNCED", "integrity_score": 1.0}