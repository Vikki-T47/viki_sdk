from typing import List, Dict
import re

class ValueConsistencyInspector:
    def __init__(self):
        self.mandatory_dna = [
            ("со-регул", "co-regulat"), ("синхрониз", "synchroniz"),
            ("ятроген", "iatrogen"), ("экзоскелет", "exoskeleton"),
            ("энтропи", "entrop"), ("sei", "sei"), ("src", "src"),
            ("гравитац", "gravit"), ("мембран", "membrane"), ("биолог", "biolog")
        ]

    def verify_integrity(self, source_text: str, result_text: str) -> Dict:
        res_low = result_text.lower()
        src_low = source_text.lower()
        
        present_count = 0
        lost_dna = []
        for ru, en in self.mandatory_dna:
            if ru in src_low or en in src_low:
                if ru in res_low or en in res_low: present_count += 1
                else: lost_dna.append(ru)

        # Проверка формата "Тезис."
        lines = [l.strip() for l in result_text.split('\n') if len(l.strip()) > 10]
        is_format_ok = all(l.startswith("Тезис.") for l in lines) if lines else False

        dna_score = (present_count / len(self.mandatory_dna)) * 100
        
        # ЖЕСТКИЕ ПОРОГИ
        status = "SYNCED"
        if dna_score < 80 or not is_format_ok:
            status = "DESYNC" # Если меньше 80% - это полный провал
        elif dna_score < 100:
            status = "PARTIAL"

        reason = f"DNA: {int(dna_score)}%. "
        if not is_format_ok: reason += "ФОРМАТ НАРУШЕН."

        return {
            "status": status,
            "score": round(dna_score, 1),
            "lost_dna": lost_dna,
            "reason": reason.strip()
        }