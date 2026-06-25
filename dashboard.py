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
except ImportError as e:
    st.error(f"❌ System Error: {e}")
    st.stop()

VERSION = "2.0.1"
telemetry = VIKI_Telemetry()

st.set_page_config(page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}", layout="wide")
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

if 'viki' not in st.session_state:
    st.session_state.viki = VIKI_Middleware()

viki = st.session_state.viki

# --- ШАГ 0: ПРЕДВАРИТЕЛЬНЫЙ АНАЛИЗ (До отрисовки UI) ---
# Мы берем значение из стейта, чтобы оно было доступно везде
agent_input = st.text_input("Enter User Signal:", key="user_input_field")
task_context = st.selectbox("Task Context:", ["general", "technical", "emotional"], key="context_selector")

if agent_input:
    # Важно: это обновляет профиль зеркала и SEI ДО того, как мы нарисуем сайдбар
    viki.parse_agent_intent(agent_input)

# --- ШАГ 1: SIDEBAR (Теперь данные всегда свежие) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.write(f"**Version:** {VERSION}")
    
    st.subheader("🪞 Mirror Status")
    prof = viki.mirror_processor.user_profile
    st.write(f"Pace: **{'BRIEF' if prof['is_brief'] else 'NORMAL'}**")
    st.write(f"Complexity Score: **{prof['punctuation_density']:.2f}**")
    
    st.divider()
    sei = telemetry.stats.get("sei_current", 0.0)
    st.subheader("🧠 Cognitive Load (SEI)")
    st.progress(sei)
    st.markdown(f"Status: **{sei:.2f}**")
    
    if st.button("♻️ Reset Engine"):
        viki.src_context.error_count = 0
        telemetry.trigger_rest()
        st.rerun()

# --- ШАГ 2: ПАНЕЛЬ МЕТРИК ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 SEI Pulse", f"{sei:.2f}")
m3.metric("⏳ Mode", viki.src_context.mode.upper())
m4.metric("💰 Active Limit", f"${int(viki.src_policy.get_context_limits(viki.src_context).get('max_auto_transaction_usd', 0))}")
st.divider()

# --- ШАГ 3: РЕЗУЛЬТАТЫ ---
if agent_input:
    raw_ai_response = "I have analyzed your request. It seems correct according to current protocols. However, we should also verify the network latency, check the API key permissions, and ensure the target database is ready for write operations. Do you have any additional instructions for me before I initiate this task?"
    
    # Применяем фильтры
    final_output = viki.apply_behavioral_filters(raw_ai_response, task_context)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("🤖 **Parsed Intent:**")
        st.json(viki.intent_parser.parse(agent_input))
        st.write("**AI Raw Message:**")
        st.caption(raw_ai_response)
    with col_r:
        st.write("🛡️ **VIKI Behavioral Output:**")
        if "[RSA:" in final_output: st.warning(final_output)
        else: st.success(final_output)
        
        auth = viki.authorize({"amount_usd": 0}) # Упрощенный тест
        if auth["status"] == "AUTHORIZED": st.info("✅ ACTION AUTHORIZED")