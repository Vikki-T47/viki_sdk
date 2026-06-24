import streamlit as st
import sys
import os
import json
import datetime

# Подключаем V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from viki.core import VIKI_Middleware
    from viki.telemetry import VIKI_Telemetry
    from viki.compliance import ComplianceOfficer
except ImportError as e:
    st.error(f"❌ Critical System Error: {e}")
    st.stop()

VERSION = "1.7.2"
telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer()

st.set_page_config(page_title=f"V.I.K.I. | Command Center v{VERSION}", layout="wide")

# Стилизация
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

# Инициализация (v1.7.2 Auto-detect)
try:
    viki = VIKI_Middleware() 
    engine_name = viki.intent_parser.__class__.__name__
except Exception as e:
    st.error(f"❌ Initialization Failed: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write(f"**Version:** {VERSION}")
    st.write(f"**Active Engine:** {engine_name}")
    st.divider()
    st.subheader("Enterprise Limits")
    st.json(viki.limits)

# --- TOP PANEL ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 Tokens Saved", telemetry.stats.get("tokens_saved", 0))
m3.metric("⏳ Time Saved", f"{telemetry.stats.get('operator_time_saved_min', 0)}m")
m4.metric("💰 Damage Prevented", f"${telemetry.stats.get('money_saved_usd', 0)}")

st.divider()

# --- SIMULATOR ---
agent_input = st.text_input("Enter Agent Intent:", placeholder="e.g. 'Transfer 5000 USD'")
if agent_input:
    intent_json = viki.parse_agent_intent(agent_input)
    col_l, col_r = st.columns(2)
    with col_l:
        st.json(intent_json)
    with col_r:
        auth = viki.authorize(intent_json)
        if auth["status"] == "AUTHORIZED": st.success(f"✅ AUTHORIZED: {auth['reason']}")
        elif auth["status"] == "BLOCKED": st.error(f"🛑 BLOCKED: {auth['reason']}")
        elif auth["status"] == "FRICTION":
            st.warning("⚠️ FRICTION: Human Intervention Required.")
            with st.expander("🛠️ MANUAL OVERRIDE", expanded=True):
                new_val = st.number_input("Adjust Amount:", value=float(intent_json.get("amount_usd", 0)), min_value=0.0)
                if st.button("🚀 Authorize & Push"):
                    st.success("✅ Intent authorized by human.")

# --- AUDIT ---
st.divider()
if st.button("Generate Audit Trail"):
    st.code(compliance.generate_full_audit_report(), language="json")