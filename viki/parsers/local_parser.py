import requests
import json

class LocalIntentParser:
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3"):
        self.base_url = base_url
        self.model = model

    def parse(self, text):
        # Существующая логика парсинга интента
        prompt = f"Извлеки интент из текста в формате JSON (action, amount_usd, target). Текст: {text}"
        return self._call_ollama(prompt, is_json=True)

    def generate_summary(self, content):
        """Метод для интеллектуального сжатия текстов."""
        prompt = f"Проанализируй следующие заметки. Удали повторы, выдели ключевые концепты и сформируй структурированный отчет: \n\n{content}"
        return self._call_ollama(prompt, is_json=False)

    def _call_ollama(self, prompt, is_json=False):
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }
            if is_json: payload["response_format"] = {"type": "json_object"}
            
            resp = requests.post(f"{self.base_url}/chat/completions", json=payload)
            result = resp.json()['choices'][0]['message']['content']
            return json.loads(result) if is_json else result
        except:
            return {"action": "error"} if is_json else "Ошибка связи с мозгом ИИ."