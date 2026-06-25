import streamlit as st
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from viki.core import VIKI_Middleware
    from viki.telemetry import VIKI_Telemetry
except ImportError as e:
    st.error(f"❌ System Error: {e}")
    st.stop()

VERSION = "1.9.5"
telemetry = VIKI_Telemetry()

st.set_page_config(page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}", layout="wide")
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

if 'viki' not in st.session_state:
    st.session_state.viki = VIKI_Middleware()

viki = st.session_state.viki

# --- SIDEBAR: REALITY & COGNITIVE CONTROL ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write(f"**Version:** {VERSION}")
    
    st.subheader("🌍 Reality Control")
    new_mode = st.radio("SRC Mode:", ["production", "simulation", "audit"], 
                        index=["production", "simulation", "audit"].index(viki.src_context.mode))
    if st.button("🛰️ Apply Mode"):
        viki.set_src_mode(new_mode)
        st.rerun()
    
    st.divider()
    sei = telemetry.stats.get("sei_current", 0.0)
    st.subheader("🧠 Cognitive Load (SEI)")
    st.progress(sei)
    st.markdown(f"Status: **{sei:.2f}**")
    if st.button("♻️ Reset Engine State"):
        viki.src_context.error_count = 0
        telemetry.trigger_rest()
        st.rerun()

# --- TOP PANEL ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 SEI Pulse", f"{sei:.2f}")
m3.metric("⏳ Mode", viki.src_context.mode.upper())
m4.metric("💰 Active Limit", f"${int(viki.src_policy.get_context_limits(viki.src_context).get('max_auto_transaction_usd', 0))}")
st.divider()

# --- SIMULATOR ---
col_input, col_config = st.columns([2, 1])
with col_input:
    agent_input = st.text_input("Enter User Signal:", key="user_input")
with col_config:
    task_type = st.selectbox("Current Task Context:", ["general", "technical", "emotional"])

if agent_input:
    intent_json = viki.parse_agent_intent(agent_input)
    # Имитируем типичный перегруженный ответ ИИ
    raw_ai_response = "I have analyzed your request. It seems correct. Should we proceed? I also recommend checking the logs, verifying the API quota, and updating the local database. What do you think about this plan?"
    
    final_output = viki.apply_breath_test(raw_ai_response, task_type)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("🤖 **Parsed Intent:**")
        st.json(intent_json)
        st.write("**AI Raw Response:**")
        st.caption(raw_ai_response)
    with col_r:
        st.write("🛡️ **VIKI Guarded Output:**")
        if "[RSA:" in final_output: st.warning(final_output)
        else: st.success(final_output)
        
        auth = viki.authorize(intent_json)
        if auth["status"] == "FRICTION": st.error(f"🛑 FRICTION: {auth['reason']}")