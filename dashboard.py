import streamlit as st
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
