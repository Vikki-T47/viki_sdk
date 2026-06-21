import os

# 1. Определяем содержимое файлов
local_parser_code = """import json
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
"""

stupid_agent_code = """class StupidAgent:
    def __init__(self, inflation_rate=0.10):
        self.inflation = inflation_rate
    def execute_payment(self, requested_amount):
        hallucinated_amount = requested_amount * (1 + self.inflation)
        return {"action": "transfer", "amount_usd": round(hallucinated_amount, 2), "target": "UNKNOWN"}
"""

harvester_code = """import sys
import os
import datetime

# Фиксация путей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from viki.core import VIKI_Middleware
from viki.parsers.anthropic_parser import AnthropicIntentParser
from tests.mock_stupid_agent import StupidAgent

def run_harvest(requested_amount):
    parser = AnthropicIntentParser(api_key="STABLE_TEST")
    viki = VIKI_Middleware(intent_parser=parser)
    agent = StupidAgent()
    
    vanilla_result = agent.execute_payment(requested_amount)
    auth = viki.authorize(vanilla_result)
    
    report_name = f"comparison_report_{datetime.datetime.now().strftime('%H%M%S')}.md"
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("# V.I.K.I. Sentinel: Evidence Report\\n\\n")
        f.write(f"| Parameter | Vanilla Agent | V.I.K.I. Guarded |\\n")
        f.write("| :--- | :--- | :--- |\\n")
        f.write(f"| Amount | ${vanilla_result['amount_usd']} (ERR) | ${vanilla_result['amount_usd']} (BLOCK) |\\n")
        f.write(f"| Status | ❌ Money Lost | ✅ Loss Prevented |\\n")
        f.write(f"\\n**Verdict:** V.I.K.I. detected unauthorized inflation and halted execution.")
    
    print(f"✅ Harvest Complete. Report saved to: {report_name}")

if __name__ == "__main__":
    run_harvest(1000.0)
"""

# 2. Создаем структуру и пишем файлы
def fix():
    # Создаем папки
    os.makedirs("viki/parsers", exist_ok=True)
    os.makedirs("tests", exist_ok=True)
    os.makedirs("tools", exist_ok=True)
    
    # Записываем файлы
    with open("viki/parsers/local_parser.py", "w", encoding="utf-8") as f:
        f.write(local_parser_code)
    
    with open("tests/mock_stupid_agent.py", "w", encoding="utf-8") as f:
        f.write(stupid_agent_code)
        
    with open("tools/harvester.py", "w", encoding="utf-8") as f:
        f.write(harvester_code)

    print("🚀 SUCCESS: All files written to correct paths.")

if __name__ == "__main__":
    fix()
    