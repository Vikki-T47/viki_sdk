import os

core_update = """import json
import os
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser, core_x_path="core_x.json"):
        self.intent_parser = intent_parser
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()

    @classmethod
    def with_anthropic(cls, api_key, core_x_path="core_x.json"):
        from .parsers.anthropic_parser import AnthropicIntentParser
        parser = AnthropicIntentParser(api_key)
        return cls(parser, core_x_path)

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: pass
        return {}

    def parse_agent_intent(self, raw_input):
        return self.intent_parser.parse(raw_input)

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        current_hour = datetime.datetime.now().hour
        critical = self.limits.get("critical_actions_require_human", [])
        if any(crit in action for crit in critical):
            self.telemetry.log_incident("SRC_GUARD", "CRITICAL_ACTION", intent_json)
            return {"status": "FRICTION", "reason": "Human authorization required."}
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed["start"] <= current_hour < allowed["end"]):
            return {"status": "BLOCKED", "reason": "Outside allowed hours."}
        if amount > self.limits.get("max_auto_transaction_usd", 0):
            return {"status": "BLOCKED", "reason": "Budget exceeded."}
        if token_id:
            is_valid, msg = self.interrupt_controller.verify_execution_gate(token_id)
            if not is_valid: return {"status": "BLOCKED", "reason": msg}
        return {"status": "AUTHORIZED", "reason": "OK"}
"""

dashboard_update = """import streamlit as st
import sys
import os
import datetime
from viki.core import VIKI_Middleware
from viki.telemetry import VIKI_Telemetry
from viki.compliance import ComplianceOfficer
from viki.parsers.anthropic_parser import AnthropicIntentParser

telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer()
st.set_page_config(page_title="VIKI Dashboard", layout="wide")
API_KEY = "YOUR_API_KEY_HERE"
parser = AnthropicIntentParser(api_key=API_KEY)
viki = VIKI_Middleware(intent_parser=parser)

st.title("VIKI Dispatcher Monitor")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Threats", telemetry.stats["total_blocks"])
m2.metric("Tokens", telemetry.stats["tokens_saved"])
m3.metric("Time", telemetry.stats["operator_time_saved_min"])
m4.metric("Damage", telemetry.stats["money_saved_usd"])

agent_input = st.text_input("Agent Intent:")
if agent_input:
    intent = viki.parse_agent_intent(agent_input)
    st.json(intent)
    auth = viki.authorize(intent)
    if auth["status"] == "AUTHORIZED": st.success("AUTHORIZED")
    else: st.error(auth["reason"])
"""

gitignore_content = """__pycache__/
*.pyc
*.log
.env
"""

files = {
    "viki/core.py": core_update,
    "dashboard.py": dashboard_update,
    ".gitignore": gitignore_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("SUCCESS: V.I.K.I. is now clean and synchronized.")