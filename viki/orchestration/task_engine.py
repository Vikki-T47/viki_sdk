import os, datetime, re
from typing import List, Dict

class TaskOrchestrator:
    def __init__(self, viki_core):
        self.viki = viki_core

    def assemble_theses(self, sources: List[str], retry_msg: str = "") -> str:
        combined_source = "\n".join(sources)
        prompt = f"""
ЗАДАЧА: Сжать предоставленный текст до 4–7 ключевых тезисов.
ПИШИ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ.

ФОРМАТ ВЫВОДА:
Тезис. Краткая формулировка.
Тезис. Краткая формулировка.

ПРАВИЛА:
- Каждый тезис — одно предложение.
- Не добавляй пояснений, вступлений или заключений.
- Обязательно используй термины: ятрогения, со-регуляция, экзоскелет, энтропия.
- Каждый тезис начинай со слова "Тезис."

{retry_msg}

ТЕКСТ:
{combined_source[:6000]}
"""
        return self.viki.intent_parser._call_ollama(prompt, is_json=False)