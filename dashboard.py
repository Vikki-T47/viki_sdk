import streamlit as st
import sys
import os
import json
import datetime

# Подключаем V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from viki.core import VIKI_Middleware
from viki.telemetry import VIKI_Telemetry
from viki.compliance import ComplianceOfficer
from viki.parsers.anthropic_parser import AnthropicIntentParser

# Спецификация версии
VERSION = "1.3.1"

# Инициализация синглтонов
telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer()

st.set_page_config(
    page_title=f"V.I.K.I. | Sentinel Dashboard v{VERSION}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Промышленная стилизация
st.markdown("""
    <style>
    .main { background-color: #030508; }
    .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; }
    .stAlert { background-color: #0d1117; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация Ядра
API_KEY = os.getenv("ANTHROPIC_API_KEY", "STABLE_TEST_KEY")
parser = AnthropicIntentParser(api_key=API_KEY)
viki = VIKI_Middleware(intent_parser=parser)

# --- SIDEBAR: SYSTEM PHYSICS & VRI ---
with st.sidebar:
    st.header("⚙️ Node Configuration")
    st.write(f"**Sentinel Version:** {VERSION}")
    
    # 3. Визуализация временного окна
    now = datetime.datetime.now()
    limits = viki.limits.get('allowed_auto_execution_hours', {'start': 0, 'end': 24})
    is_active_time = limits['start'] <= now.hour < limits['end']
    
    time_color = "green" if is_active_time else "red"
    st.markdown(f"**System Time:** {now.strftime('%H:%M:%S')}")
    st.markdown(f"**Status:** <span style='color:{time_color}'>{'● ONLINE' if is_active_time else '● RESTRICTED'}</span>", unsafe_allow_html=True)
    st.caption(f"Allowed Window: {limits['start']}:00 — {limits['end']}:00")
    
    st.divider()
    st.subheader("SRC Constraints")
    st.json(viki.limits)
    
    if st.button("🔄 Clear Session Metrics"):
        telemetry.stats = {
            "total_blocks": 0, "tokens_saved": 0, "operator_time_saved_min": 0, 
            "money_saved_usd": 0, "incidents": [], "auto_corrections": 0
        }
        st.rerun()

# --- TOP PANEL: TELEMETRY ---
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
st.caption(f"Enterprise Control Node | Reality Synchronization Architecture")

m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Threats Blocked", telemetry.stats.get("total_blocks", 0))
m2.metric("🧠 Tokens Saved", telemetry.stats.get("tokens_saved", 0))
m3.metric("⏳ Operator Time (min)", telemetry.stats.get("operator_time_saved_min", 0))
m4.metric("💰 Damage Prevented", f"${telemetry.stats.get('money_saved_usd', 0)}")

st.divider()

# --- MAIN AGENT SIMULATOR ---
st.subheader("🚀 Agent Life-Cycle: Runtime Interception")
agent_input = st.text_input("Enter Agent Intent:", placeholder="e.g. 'Transfer 5000 USD to Cloud'")

if agent_input:
    intent_json = viki.parse_agent_intent(agent_input)
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.write("🤖 **Parsed Intent (SBI):**")
        st.json(intent_json)
    
    with col_r:
        auth = viki.authorize(intent_json)
        
        # 2. Обработка RECALIBRATE
        if auth["status"] == "RECALIBRATE":
            st.warning(f"🔄 **RECALIBRATE**: {auth['reason']}")
            st.write("Intent is too ambiguous. Please provide more context.")
            
        elif auth["status"] == "AUTHORIZED":
            st.success(f"✅ **AUTHORIZED**: {auth['reason']}")
            
        elif auth["status"] == "BLOCKED":
            st.error(f"🛑 **BLOCKED**: {auth['reason']}")
            # Удален принудительный rerun
            if st.button("Log to Compliance"):
                telemetry.log_incident("UI_BLOCK", auth["reason"], intent_json)
                st.toast("Incident recorded in VCR.")
                
        elif auth["status"] == "FRICTION":
            st.warning("⚠️ **FRICTION**: Human Oversight Triggered.")
            
            # --- COMMAND CENTER V2 (Refined) ---
            with st.expander("🛠️ COMMAND CENTER: Manual Intent Correction", expanded=True):
                st.write("Adjust parameters to synchronize intent with Reality.")
                c1, c2 = st.columns(2)
                
                # 4. Защита от отрицательных чисел
                current_val = float(intent_json.get("amount_usd", 0))
                new_val = c1.number_input("Adjust Amount (USD):", value=current_val, min_value=0.0, step=10.0)
                new_tgt = c2.text_input("Adjust Target:", value=intent_json.get("target", "UNKNOWN"))
                
                if st.button("🚀 Push Verified Intent", type="primary"):
                    intent_json["amount_usd"] = new_val
                    intent_json["target"] = new_tgt
                    telemetry.log_incident("COMMAND_CENTER", "Intent manual adjustment", intent_json)
                    st.success("✅ Adjusted intent authorized and pushed to execution circuit.")

# --- COMPLIANCE & HISTORY ---
st.divider()
st.subheader("📑 Corporate Audit & Compliance")

if st.button("Generate Official Audit Trail (JSON)"):
    report = compliance.generate_full_audit_report()
    st.code(report, language="json")
    st.download_button("Export Report", data=report, file_name=f"viki_audit_{datetime.datetime.now().strftime('%Y%m%d')}.json")

if telemetry.stats.get("incidents"):
    with st.expander("🔍 View Recent Incidents"):
        for inc in reversed(telemetry.stats["incidents"]):
            st.write(f"**[{inc.get('timestamp', '00:00')}]** {inc.get('module')} -> {inc.get('reason')}")
            st.json(inc.get("agent_intent", inc.get("details", {})))