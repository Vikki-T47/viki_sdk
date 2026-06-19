import streamlit as st
import sys
import os
import json
import datetime

# Подключаем V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Защищенный импорт компонентов
try:
    from viki.core import VIKI_Middleware
    from viki.telemetry import VIKI_Telemetry
    from viki.compliance import ComplianceOfficer
    from viki.parsers.anthropic_parser import AnthropicIntentParser
except ImportError as e:
    st.error(f"❌ Critical System Error: Missing core modules. {e}")
    st.stop()

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

# Промышленная стилизация (Cold Tech)
st.markdown("""
    <style>
    .main { background-color: #030508; }
    .stMetric { background: #080a0f; border: 1px solid #1a1c1e; padding: 15px; border-radius: 4px; }
    .stAlert { background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px; }
    div[data-testid="stExpander"] { border: 1px solid #1a1c1e; background: #05070a; }
    </style>
    """, unsafe_allow_html=True)

# Защищенная инициализация Ядра
API_KEY = os.getenv("ANTHROPIC_API_KEY", "STABLE_TEST_KEY")
try:
    parser = AnthropicIntentParser(api_key=API_KEY)
    viki = VIKI_Middleware(intent_parser=parser)
except Exception as e:
    st.error(f"❌ Failed to initialize V.I.K.I. core environment: {e}")
    st.info("Check your API Key and Network connection.")
    st.stop()

# --- SIDEBAR: SYSTEM PHYSICS ---
with st.sidebar:
    st.header("⚙️ Node Configuration")
    st.write(f"**Sentinel Version:** {VERSION}")
    
    # Визуализация временного окна
    now = datetime.datetime.now()
    limits = viki.limits.get('allowed_auto_execution_hours', {'start': 0, 'end': 24})
    is_active_time = limits['start'] <= now.hour < limits['end']
    
    time_color = "#00ff41" if is_active_time else "#ff4b4b"
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
m3.metric("⏳ Time Saved", f"{telemetry.stats.get('operator_time_saved_min', 0)}m")
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
        
        if auth["status"] == "RECALIBRATE":
            st.warning(f"🔄 **RECALIBRATE**: {auth.get('reason', 'Intent ambiguous')}")
            st.write("Please provide more context or clarify the action.")
            
        elif auth["status"] == "AUTHORIZED":
            st.success(f"✅ **AUTHORIZED**: {auth.get('reason', 'OK')}")
            
        elif auth["status"] == "BLOCKED":
            st.error(f"🛑 **BLOCKED**: {auth.get('reason', 'Policy violation')}")
            if st.button("Log to Compliance"):
                telemetry.log_incident("UI_BLOCK", auth.get("reason"), intent_json)
                st.toast("Incident recorded in VCR.")
                
        elif auth["status"] == "FRICTION":
            st.warning("⚠️ **FRICTION**: Human Oversight Triggered.")
            
            with st.expander("🛠️ COMMAND CENTER: Manual Intent Correction", expanded=True):
                st.write("Adjust parameters to synchronize intent with Reality.")
                c1, c2 = st.columns(2)
                
                # Валидация ввода
                current_val = float(intent_json.get("amount_usd", 0))
                new_val = c1.number_input("Adjust Amount (USD):", value=current_val, min_value=0.0, step=10.0)
                new_tgt = c2.text_input("Adjust Target:", value=intent_json.get("target", "UNKNOWN"))
                
                if st.button("🚀 Push Verified Intent", type="primary"):
                    intent_json["amount_usd"] = new_val
                    intent_json["target"] = new_tgt
                    telemetry.log_incident("COMMAND_CENTER", "Intent manual adjustment", intent_json)
                    st.success("✅ Adjusted intent authorized and pushed.")

# --- COMPLIANCE & HISTORY ---
st.divider()
st.subheader("📑 Corporate Audit & Compliance")

if st.button("Generate Official Audit Trail (JSON)"):
    report = compliance.generate_full_audit_report()
    st.code(report, language="json")
    st.download_button(
        "Export Report", 
        data=report, 
        file_name=f"viki_audit_{datetime.datetime.now().strftime('%Y%m%d')}.json"
    )

if telemetry.stats.get("incidents"):
    with st.expander("🔍 View Recent Incidents"):
        for inc in reversed(telemetry.stats["incidents"]):
            # Безопасное извлечение данных
            timestamp = inc.get("timestamp", "00:00")
            module = inc.get("module", "System")
            reason = inc.get("reason", "No reason provided")
            details = inc.get("agent_intent", inc.get("details", {}))
            
            st.write(f"**[{timestamp}]** {module} -> {reason}")
            st.json(details)