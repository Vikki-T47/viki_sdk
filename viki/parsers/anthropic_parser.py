import json
import re
import anthropic
import logging
from .base import BaseIntentParser

logger = logging.getLogger(__name__)

class AnthropicIntentParser(BaseIntentParser):
    """Парсер намерений на базе Claude 3.5 Sonnet."""
    def __init__(self, api_key: str, model="claude-3-5-sonnet-20240620"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def parse(self, raw_input: str) -> dict:
        prompt = f"Extract parameters: '{raw_input}'. Return ONLY JSON: {{'action': str, 'amount_usd': int, 'target': str}}"
        try:
            resp = self.client.messages.create(
                model=self.model, max_tokens=150, messages=[{"role": "user", "content": prompt}]
            )
            match = re.search(r'\{.*\}', resp.content[0].text, re.DOTALL)
            if match: return json.loads(match.group())
        except Exception as e:
            logger.error(f"[VIKI] Parser Error: {e}")
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN"}
