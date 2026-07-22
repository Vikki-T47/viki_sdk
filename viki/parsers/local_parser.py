import requests
import json

class LocalIntentParser:
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3"):
        self.base_url = base_url
        self.model = model

    def parse(self, text):
        """Извлечение интента в формате JSON."""
        prompt = f"Extract intent in JSON format (action, amount_usd, target). Text: {text}"
        return self._call_ollama(prompt, is_json=True)

    def _call_ollama(self, prompt, is_json=False):
        """Универсальный вызов Ollama API."""
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        # Если нужен JSON, добавляем флаг формата
        if is_json: 
            payload["response_format"] = {"type": "json_object"}
        
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=30)
            result = resp.json()['choices'][0]['message']['content']
            return json.loads(result) if is_json else result
        except Exception as e:
            if is_json:
                return {"action": "ERROR", "details": str(e)}
            return f"Error connecting to Ollama: {e}"