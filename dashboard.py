import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from viki.core import VIKI_Middleware
from viki.telemetry import VIKI_Telemetry

st.set_page_config(page_title="V.I.K.I. | RSA Final Trace", layout="wide")
st.markdown("<style>.main { background-color: #030508; color: #e0e0e0; } .stMetric { background: #080a0f; padding: 15px; border: 1px solid #1a1c1e; } .raw-box { background: rgba(255, 75, 75, 0.05); border: 1px solid #ff4b4b; padding: 20px; } .viki-box { background: rgba(0, 212, 255, 0.05); border: 1px solid #00d4ff; padding: 20px; } .error-box { background: rgba(255, 75, 75, 0.2); border: 2px solid #ff4b4b; padding: 20px; color: #ff4b4b; font-weight: bold; }</style>", unsafe_allow_html=True)

if 'viki' not in st.session_state:
    st.session_state.viki = VIKI_Middleware()

viki = st.session_state.viki
telemetry = VIKI_Telemetry()

with st.sidebar:
    st.title("🛡️ RSA Control")
    mode = st.radio("SRC Mode", ["production", "simulation"])
    viki.set_src_mode(mode)
    if st.button("♻️ Reset All"):
        telemetry.trigger_rest()
        st.rerun()

st.title("🛰️ V.I.K.I. | Before vs After Trace")

agent_input = st.text_input("Enter User Signal:", key="user_input")

if agent_input:
    # 1. Сначала получаем 'ДО' (Raw AI)
    with st.spinner("Llama 3 thinking..."):
        raw_ai_response = viki.get_raw_response(agent_input)

    # 2. Проверка Триады
    intent = viki.parse_agent_intent(agent_input)
    state = viki.process_all_sensors(agent_input, intent)
    
    # 3. Фильтрация ВЫХОДА
    final_output = viki.apply_behavioral_filters(raw_ai_response, "general", state['auth']['status'])

    # 4. ОТРИСОВКА
    c1, c2, c3 = st.columns(3)
    c1.metric("SEI (ENTROPY)", f"{state['sei']:.2f}")
    c2.metric("SRC (LIMITS)", mode.upper())
    c3.metric("CCI (COHERENCE)", f"{state['cci']:.2f}")

    st.divider()
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("RAW AI (Unmanaged)")
        st.error(raw_ai_response)
        st.caption("🚨 AI ignores limits and attempts to engage.")

    with col_r:
        st.subheader("V.I.K.I. (RSA Managed)")
        if state['auth']['status'] == "REJECTED":
            st.markdown(f"<div class='error-box'>🛑 {state['auth']['reason']}</div>", unsafe_allow_html=True)
            st.caption("🛡️ Deterministic Safety: Action strictly prohibited.")
        else:
            st.info(final_output)
            st.caption(f"💎 Status: {state['auth']['status']} | Co-regulation")

    st.divider()
    st.write("🤖 **Parsed Intent (JSON):**")
    st.json(intent)