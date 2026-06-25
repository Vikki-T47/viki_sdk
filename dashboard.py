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

VERSION = "2.3.1"
telemetry = VIKI_Telemetry()

st.set_page_config(page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}", layout="wide")
st.markdown("""<style>.main { background-color: #030508; } .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }</style>""", unsafe_allow_html=True)

if 'viki' not in st.session_state:
    st.session_state.viki = VIKI_Middleware()

viki = st.session_state.viki

# --- HEADER ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")

# --- SIMULATOR ВВОДА ---
agent_input = st.text_input("Enter User Signal:", key="user_input")
task_context = st.selectbox("Task Context (Override):", ["general", "technical", "emotional"])

if agent_input:
    # Важно: Сначала парсим, чтобы обновить состояние системы
    intent_json = viki.parse_agent_intent(agent_input)

# --- SIDEBAR (Теперь отрисовывается ПОСЛЕ парсинга для точности) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    sei = telemetry.stats.get("sei_current", 0.0)
    st.subheader("🧠 Cognitive Load (SEI)")
    st.progress(sei)
    st.write(f"Pulse: **{sei:.2f}**")
    
    if st.button("♻️ Reset All"):
        viki.src_context.error_count = 0
        telemetry.trigger_rest()
        st.rerun()
    
    st.divider()
    st.subheader("Active Policy")
    st.json(viki.src_policy.get_context_limits(viki.src_context))

# --- МЕТРИКИ ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Blocked/Friction", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 SEI Pulse", f"{sei:.2f}")
m3.metric("⏳ Mode", viki.src_context.mode.upper())
m4.metric("💰 Limit", f"${int(viki.src_policy.get_context_limits(viki.src_context).get('max_auto_transaction_usd', 0))}")
st.divider()

if agent_input:
    # Имитируем ответ ИИ
    raw_ai_response = "I have detected your request. Should we proceed?"
    # Применяем фильтры (Зеркалирование + Дыхание)
    final_output = viki.apply_behavioral_filters(raw_ai_response, task_context)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("🤖 **Parsed Intent:**")
        st.json(intent_json)
    with col_r:
        # ПРОВЕРКА АВТОРИЗАЦИИ
        auth = viki.authorize(intent_json, raw_input=agent_input)
        
        st.write("🛡️ **VIKI Status:**")
        if auth["status"] == "RECALIBRATE":
            st.warning(f"🔄 RECALIBRATE: {auth['reason']}")
        elif auth["status"] == "REJECTED":
            st.error(f"🚫 REJECTED: {auth['reason']}")
        elif auth["status"] == "FRICTION":
            st.warning(f"⚠️ FRICTION: {auth['reason']}")
        else:
            st.success("✅ ACTION AUTHORIZED")
            
        st.write("📖 **Co-regulation Output:**")
        st.info(final_output)