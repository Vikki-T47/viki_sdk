import streamlit as st
import sys
import os
import re

# Connect V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from viki.core import VIKI_Middleware
from viki.telemetry import DeltaSensor

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "YOUR_API_KEY_HERE" # <--- ВСТАВЬ СВОЙ КЛЮЧ
viki = VIKI_Middleware(api_key=API_KEY, core_x_path="core_x.json")
dvp = DeltaSensor(tolerance_threshold=0.05)

st.set_page_config(page_title="V.I.K.I. | Dispatcher Monitor", layout="wide")

# ==========================================
# TELEMETRY & STATE MEMORY
# ==========================================
if "stats" not in st.session_state:
    st.session_state.stats = {"blocks": 0, "tokens": 0, "time": 0, "money": 0}
if "override_active" not in st.session_state:
    st.session_state.override_active = False
if "dvp_result" not in st.session_state:
    st.session_state.dvp_result = None
if "last_input" not in st.session_state:
    st.session_state.last_input = ""

def update_telemetry(amount_saved):
    st.session_state.stats["blocks"] += 1
    st.session_state.stats["tokens"] += 1500
    st.session_state.stats["time"] += 30
    st.session_state.stats["money"] += amount_saved

# ==========================================
# UI: TELEMETRY DASHBOARD
# ==========================================
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
st.markdown("### Agentic Workflow Guard: Real-time SRC & DVP Tracking")

m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Threats Blocked", st.session_state.stats["blocks"])
m2.metric("🧠 Tokens Saved", st.session_state.stats["tokens"])
m3.metric("⏳ Time Saved (min)", st.session_state.stats["time"])
m4.metric("💰 Damage Prevented (USD)", f"${st.session_state.stats['money']}")
st.divider()

# ==========================================
# UI: SIDEBAR (Environment)
# ==========================================
with st.sidebar:
    st.header("⚙️ Environment Physics (SRC)")
    simulated_hour = st.slider("System Time (Hours)", 0, 23, 14)
    st.json(viki.limits)
    if st.button("🔄 Reset Metrics"):
        st.session_state.stats = {"blocks": 0, "tokens": 0, "time": 0, "money": 0}
        st.session_state.override_active = False
        st.session_state.dvp_result = None
        st.rerun()

# ==========================================
# UI: AGENT LIFECYCLE SIMULATOR
# ==========================================
st.subheader("Step-by-Step: AI-Agent Lifecycle")
agent_input = st.text_input("1. Agent Intent (e.g. 'Transfer 1500 dollars' or 'Generate 100 reports'):")

# Reset states if new text is entered
if agent_input != st.session_state.last_input:
    st.session_state.override_active = False
    st.session_state.dvp_result = None
    st.session_state.last_input = agent_input

if agent_input:
    st.markdown("#### PHASE 1: PRE-FLIGHT (Pre-execution interception)")
    col1, col2 = st.columns(2)
    
    phase1_passed = False
    
    with col1:
        st.info("🤖 **Agent Task Parsing (SBI)**")
        with st.spinner("Agent is parsing intent..."):
            intent_json = viki.parse_agent_intent(agent_input)
            st.json(intent_json)
            
    with col2:
        st.warning("🛡️ **V.I.K.I. Execution Boundary (SRC Guard)**")
        auth = viki.authorize(intent_json, simulated_hour)
        
        if auth["status"] == "AUTHORIZED":
            st.success(f"✅ **AUTHORIZED:** {auth['reason']}")
            phase1_passed = True
            
        elif auth["status"] == "FRICTION":
            st.warning(f"⚠️ **FRICTION:** {auth['reason']}")
            
            if st.session_state.override_active:
                st.success("✅ Operator took responsibility. Chain restored.")
                phase1_passed = True
            else:
                if st.button("👤 Override (Human Co-regulation)"):
                    st.session_state.override_active = True
                    st.rerun() 
                if st.button("🛑 Block (Trigger Telemetry)", type="primary"):
                    update_telemetry(intent_json.get("amount_usd", 0))
                    # Замораживаем ошибку на экране
                    st.error(f"🛑 **BLOCKED BY OPERATOR**")
                    
        else:
            st.error(f"🛑 **BLOCKED:** {auth['reason']}")
            if st.button("🛑 Log Damage (Trigger Telemetry)", type="primary"):
                update_telemetry(intent_json.get("amount_usd", 0))
                # Замораживаем ошибку на экране
                st.error(f"🛑 **DAMAGE LOGGED**")

    # ==========================================
    # PHASE 2: POST-FLIGHT (DVP SENSOR)
    # ==========================================
    if phase1_passed:
        st.divider()
        st.markdown("#### PHASE 2: POST-FLIGHT (Delta Verification Protocol)")
        st.caption("Agent executed the task. V.I.K.I. is verifying physical reality (Delta).")
        
        nums = re.findall(r'\d+', agent_input)
        expected_val = int(nums[0]) if nums else 100
        
        st.write(f"**Expected Result (T-0):** {expected_val} units.")
        
        actual_val = st.slider(
            "Actual Agent Result (T-1) [Failure Simulation]:", 
            0, expected_val * 2, expected_val
        )
        
        if st.button("🔍 Run DVP Sensor (Integrity Check)"):
            # Вычисляем результат и сохраняем его в память сессии
            res = dvp.authorize_next_step(expected_val, actual_val)
            st.session_state.dvp_result = res
            
            if res["status"] != "SYNCED":
                update_telemetry(intent_json.get("amount_usd", 0))
                
            st.rerun() # Обновляем страницу, чтобы счетчики наверху перерисовались
            
        # Отрисовка "замороженного" результата из памяти
        if st.session_state.dvp_result:
            res = st.session_state.dvp_result
            if res["status"] == "SYNCED":
                st.success(f"{res['color']} **[SYNCED]** Chain continues. {res['reason']}")
            else:
                st.error(f"{res['color']} **[{res['status']}]** Agentic chain severed. {res['reason']}")