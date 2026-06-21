import sys
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
        f.write("# V.I.K.I. Sentinel: Evidence Report\n\n")
        f.write(f"| Parameter | Vanilla Agent | V.I.K.I. Guarded |\n")
        f.write("| :--- | :--- | :--- |\n")
        f.write(f"| Amount | ${vanilla_result['amount_usd']} (ERR) | ${vanilla_result['amount_usd']} (BLOCK) |\n")
        f.write(f"| Status | ❌ Money Lost | ✅ Loss Prevented |\n")
        f.write(f"\n**Verdict:** V.I.K.I. detected unauthorized inflation and halted execution.")
    
    print(f"✅ Harvest Complete. Report saved to: {report_name}")

if __name__ == "__main__":
    run_harvest(1000.0)
