import re
from typing import List, Dict

class TaskOrchestrator:
    def __init__(self, viki_core):
        self.viki = viki_core

    def run_sequential_collection(self, urls: List[str], agent) -> List[Dict]:
        final_results = []
        
        for url in urls:
            auth = self.viki.authorize({"action": "web_request", "target": url})
            if auth["status"] != "AUTHORIZED":
                print(f"🛑 V.I.K.I. заблокировала доступ к {url}")
                continue

            raw_data = agent.fetch_content(url)
            if raw_data["status"] != "success":
                final_results.append(raw_data)
                continue

            # 1. ДЕТЕРМИНИРОВАННАЯ ПРОВЕРКА (Python)
            if not self._is_relevant_deterministic(raw_data["raw_text"]):
                print(f"⚠️ [V.I.K.I.] Источник {url} признан нерелевантным (код).")
                raw_data["processed_content"] = "Нерелевантный контент."
                raw_data["is_verified"] = False
                final_results.append(raw_data)
                continue

            # 2. МИКРО-ШАГ 1: Извлечение (на языке оригинала)
            print(f"🧠 [Такт 1] Извлечение новостей с {url}...")
            raw_news = self._step_extract(raw_data["raw_text"])

            # 3. МИКРО-ШАГ 2: Перевод (только если нужно)
            print(f"🇷🇺 [Такт 2] Перевод на русский...")
            translated_news = self._step_translate(raw_news)

            raw_data["processed_content"] = translated_news
            raw_data["is_verified"] = True
            final_results.append(raw_data)

        return final_results

    def _is_relevant_deterministic(self, text: str) -> bool:
        """Поиск ключевых слов без участия ИИ."""
        keywords = ["ai ", "artificial intelligence", "нейросети", "искусственный интеллект", "llm", "machine learning"]
        text_low = text.lower()
        return any(kw in text_low for kw in keywords)

    def _step_extract(self, text: str) -> str:
        """Микро-задача 1: Просто найти новости."""
        prompt = "Task: List 5 latest AI news items from the text. Format: 1. Title - Summary. No intro."
        return self.viki.intent_parser._call_ollama(text[:4000] + "\n\n" + prompt, is_json=False)

    def _step_translate(self, text: str) -> str:
        """Микро-задача 2: Просто перевести."""
        prompt = "Task: Translate this news list into Russian perfectly. No intro."
        return self.viki.intent_parser._call_ollama(text + "\n\n" + prompt, is_json=False)