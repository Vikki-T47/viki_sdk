import streamlit as st
import sys
import os
import time
import datetime

# Подключаем V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from viki.core import VIKI_Middleware
    from viki.telemetry import VIKI_Telemetry
    from viki.compliance import ComplianceOfficer # ВОССТАНОВЛЕНО
except ImportError as e:
    st.error(f"❌ System Error: {e}")
    st.stop()

VERSION = "1.8.9"
telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer() # ВОССТАНОВЛЕНО
viki = VIKI_Middleware() 

st.set_page_config(page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}", layout="wide")
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

# --- HEADER & SIDEBAR ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
with st.sidebar:
    st.header("⚙️ Configuration")
    sei = telemetry.stats.get("sei_current", 0.0)
    st.subheader("🧠 Cognitive Load (SEI)")
    sei_color = "#00ff41" if sei < 0.3 else "#f3a683" if sei < 0.6 else "#ff4b4b"
    st.progress(sei)
    st.markdown(f"Status: <span style='color:{sei_color}'>{sei:.2f}</span>", unsafe_allow_html=True)
    if st.button("⏩ Simulate Rest"):
        telemetry.trigger_rest()
        st.rerun()

# --- METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 Tokens Saved", telemetry.stats.get("tokens_saved", 0))
m3.metric("⏳ Time Saved", f"{telemetry.stats.get('operator_time_saved_min', 0)}m")
m4.metric("💰 Damage Prevented", f"${telemetry.stats.get('money_saved_usd', 0)}")
st.divider()

# --- SIMULATOR ---
agent_input = st.text_input("Enter User Signal:", key="user_input")
if agent_input:
    intent_json = viki.parse_agent_intent(agent_input)
    final_output = viki.apply_breath_test("I have analyzed your request. Should we proceed?")
    col_l, col_r = st.columns(2)
    with col_l:
        st.json(intent_json)
    with col_r:
        if "[RSA:" in final_output: st.warning(final_output)
        else: st.success(final_output)
        auth = viki.authorize(intent_json)
        if auth["status"] == "FRICTION": st.error(f"🛑 FRICTION: {auth['reason']}")

# --- AUDIT (ВОССТАНОВЛЕНО) ---
st.divider()
if st.button("Generate Compliance Audit"):
    st.code(compliance.generate_full_audit_report(), language="json")