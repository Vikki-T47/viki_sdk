import os
import re
from typing import List, Dict, Any

class RealityPreScanner:
    """
    V.I.K.I. Reality Pre-Scanner v1.0.
    Детерминированный анализ источников для построения Карты Истины.
    """
    def __init__(self):
        # Базовый словарь ДНК для поиска (корни слов)
        self.dna_dictionary = [
            ("со-регул", "co-regulat"), ("синхрониз", "synchroniz"),
            ("ятроген", "iatrogen"), ("экзоскелет", "exoskeleton"),
            ("энтропи", "entrop"), ("sei", "sei"), ("src", "src"),
            ("гравитац", "gravit"), ("мембран", "membrane"), ("биолог", "biolog")
        ]

    def scan_sources(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Сканирует файлы и строит Task Passport v2.0.
        """
        found_dna = set()
        total_size = 0
        detected_langs = {"ru": 0, "en": 0}

        for path in file_paths:
            if not os.path.exists(path): continue
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                total_size += len(content)
                
                # 1. Поиск ДНК (Карта Истины)
                for ru_root, en_root in self.dna_dictionary:
                    if ru_root in content or en_root in content:
                        found_dna.add(ru_root) # Храним RU-корень как ключ
                
                # 2. Определение языка (простой эшелон)
                if re.search('[а-яА-Я]', content): detected_langs["ru"] += 1
                if re.search('[a-zA-Z]', content): detected_langs["en"] += 1

        # Определяем доминирующий язык
        primary_lang = "RU" if detected_langs["ru"] >= detected_langs["en"] else "EN"
        
        # 3. Выбор стратегии
        # Если файлов > 3 или объем > 5000 знаков — Step-by-Step
        strategy = "step_by_step" if len(file_paths) > 3 or total_size > 5000 else "single_pass"

        return {
            "truth_map": list(found_dna),
            "language": primary_lang,
            "strategy": strategy,
            "complexity": "HIGH" if strategy == "step_by_step" else "LOW",
            "objects_count": len(file_paths)
        }