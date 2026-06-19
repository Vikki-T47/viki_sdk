import streamlit as st
import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from viki.core import VIKI_Middleware
from viki.telemetry import VIKI_Telemetry
from viki.navigator import VikiNavigator
from viki.parsers.anthropic_parser import AnthropicIntentParser

# Инициализация
telemetry = VIKI_Telemetry()
nav = VikiNavigator()
parser = AnthropicIntentParser(api_key=os.getenv("ANTHROPIC_API_KEY", "STABLE_TEST"))
viki = VIKI_Middleware(intent_parser=parser)

st.set_page_config(page_title="V.I.K.I. Resilience Node", layout="wide")

# --- SIDEBAR: CIRCUIT BREAKER STATUS ---
with st.sidebar:
    st.header("⚙️ Node Integrity")
    if not viki.breaker.stats:
        st.info("All external services STABLE")
    for service, data in viki.breaker.stats.items():
        if data["status"] == "OPEN":
            st.error(f"🔴 ISOLATED: {service}")
        else:
            st.success(f"🟢 ACTIVE: {service}")

# --- MAIN UI ---
st.title("🛡️ V.I.K.I. Resilience Dashboard")
task_id = "DURABLE_TEST_001"
saved = nav.load_state(task_id)

if saved and saved["status"] != "COMPLETED":
    st.warning(f"⚠️ Unfinished Task: {task_id} paused at step {saved['current_step']}/{saved['total_steps']}")
    if st.button("🚀 RESUME SESSION"):
        st.info("Resuming execution path...")

# --- BLACK BOX AUDIT ---
st.divider()
st.subheader("📼 Black Box: Audit Replay")
if st.button("Analyze Trace Log"):
    trace_data = nav.replay(task_id)
    if trace_data:
        df = pd.DataFrame(trace_data, columns=["Step", "Reasoning", "Result"])
        st.table(df)
        st.download_button("Download Audit Protocol (CSV)", df.to_csv(index=False), "viki_audit_trail.csv")
    else:
        st.info("No trace data available for the current session.")