import streamlit as st
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from viki.core import VIKI_Middleware
    from viki.telemetry import VIKI_Telemetry
    from viki.compliance import ComplianceOfficer
except ImportError as e:
    st.error(f"❌ System Error: {e}")
    st.stop()

VERSION = "2.2.0"
telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer()

st.set_page_config(page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}", layout="wide")
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

if 'viki' not in st.session_state:
    st.session_state.viki = VIKI_Middleware()

viki = st.session_state.viki

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write(f"**Version:** {VERSION}")
    
    st.subheader("🌍 Reality Control")
    mode = st.radio("SRC Mode:", ["production", "simulation", "audit"], 
                    index=["production", "simulation", "audit"].index(viki.src_context.mode))
    
    if st.button("🛰️ Apply Context"):
        viki.set_src_mode(mode)
        st.rerun()

    st.divider()
    sei = telemetry.stats.get("sei_current", 0.0)
    st.progress(sei)
    st.write(f"SEI Pulse: **{sei:.2f}**")
    
    if st.button("♻️ Reset All"):
        viki.src_context.error_count = 0
        telemetry.trigger_rest()
        st.rerun()

# --- TOP PANEL ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked/Friction", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 SEI", f"{sei:.2f}")
m3.metric("⏳ Mode", viki.src_context.mode.upper())
m4.metric("💰 Limit", f"${int(viki.src_policy.get_context_limits(viki.src_context).get('max_auto_transaction_usd', 0))}")
st.divider()

# --- SIMULATOR ---
col_input, col_config = st.columns([2, 1])
with col_input:
    agent_input = st.text_input("Enter User Signal:", key="user_input")
with col_config:
    task_context = st.selectbox("Task Context:", ["general", "technical", "emotional"])

if agent_input:
    intent_json = viki.parse_agent_intent(agent_input)
    raw_ai_response = "I have analyzed your request. Should we proceed?"
    final_output = viki.apply_behavioral_filters(raw_ai_response, task_context)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("🤖 **Parsed Intent:**")
        st.json(intent_json)
    with col_r:
        auth = viki.authorize(intent_json, raw_input=agent_input)
        if auth["status"] == "REJECTED": st.error(f"🚫 REJECTED: {auth['reason']}")
        elif auth["status"] == "FRICTION": st.warning(f"⚠️ FRICTION: {auth['reason']}")
        else: st.success("✅ AUTHORIZED")
        
        st.info(final_output)

# --- AUDIT ---
st.divider()
if st.button("Generate Compliance Audit"):
    report = compliance.generate_full_audit_report()
    st.code(report, language="json")