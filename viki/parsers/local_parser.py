import json
import re
import requests
import logging
from .base import BaseIntentParser

logger = logging.getLogger(__name__)

class LocalIntentParser(BaseIntentParser):
    def __init__(self, base_url="http://localhost:11434/v1", model="llama3"):
        self.base_url = base_url
        self.model = model

    def parse(self, raw_input: str) -> dict:
        prompt = f"Extract parameters: '{raw_input}'. Return ONLY JSON: {{'action': str, 'amount_usd': int, 'target': str}}"
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0}
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, timeout=10)
            content = response.json()['choices'][0]['message']['content']
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match: return json.loads(match.group())
        except Exception: pass
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN"}
