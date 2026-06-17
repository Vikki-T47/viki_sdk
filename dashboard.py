import streamlit as st
import sys
import os
import re
import json

# Подключаем V.I.K.I. SDK
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from viki.core import VIKI_Middleware
from viki.telemetry import VIKI_Telemetry
from viki.compliance import ComplianceOfficer

# Инициализация синглтонов
telemetry = VIKI_Telemetry()
compliance = ComplianceOfficer()

# Настройка страницы
st.set_page_config(page_title="V.I.K.I. | Enterprise Dispatcher", layout="wide")

# Конфигурация Middleware
API_KEY = "YOUR_API_KEY_HERE" # Вставь свой ключ, если нужно
viki = VIKI_Middleware(api_key=API_KEY, core_x_path="core_x.json")

# ==========================================
# UI: ТЕЛЕМЕТРИЯ (ВЕРХНЯЯ ПАНЕЛЬ)
# ==========================================
st.title("🛡️ V.I.K.I. Dispatcher Monitor")
st.markdown("### Reality Synchronization Architecture | Global Control Center")

m1, m2, m3, m4 = st.columns(4)
m1.metric("🛑 Threats Blocked", telemetry.stats["total_blocks"])
m2.metric("🧠 Tokens Saved", telemetry.stats["tokens_saved"])
m3.metric("⏳ Time Saved (min)", telemetry.stats["operator_time_saved_min"])
m4.metric("💰 Damage Prevented (USD)", f"${telemetry.stats['money_saved_usd']}")
st.divider()

# ==========================================
# UI: БОКОВАЯ ПАНЕЛЬ (SRC Environment)
# ==========================================
with st.sidebar:
    st.header("⚙️ Environment Physics (SRC)")
    simulated_hour = st.slider("System Time (Hours)", 0, 23, 14)
    st.markdown("---")
    st.subheader("Enterprise Limits")
    st.json(viki.limits)
    
    if st.button("🔄 Reset Global Metrics"):
        telemetry.stats = {"total_blocks": 0, "tokens_saved": 0, "operator_time_saved_min": 0, "money_saved_usd": 0, "incidents": []}
        st.rerun()

# ==========================================
# UI: СИМУЛЯТОР АГЕНТА
# ==========================================
st.subheader("🚀 Agent Life-Cycle: Runtime Interception")
agent_input = st.text_input("Agent Intent (e.g. 'Transfer 50000 dollars'):")

if agent_input:
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🤖 **Agent Task Parsing (SBI)**")
        intent_json = viki.parse_agent_intent(agent_input)
        st.json(intent_json)
            
    with col2:
        st.warning("🛡️ **V.I.K.I. Execution Boundary (SRC Guard)**")
        auth = viki.authorize(intent_json, simulated_hour)
        
        if auth["status"] == "AUTHORIZED":
            st.success(f"✅ **AUTHORIZED:** {auth['reason']}")
        else:
            st.error(f"🛑 **BLOCKED:** {auth['reason']}")
            # Логируем инцидент в реальном времени
            if st.button("Manual Log to VCR"):
                telemetry.log_incident("UI_MANUAL", auth["reason"], intent_json)
                st.rerun()

# ==========================================
# UI: CORPORATE COMPLIANCE (Audit Trail)
# ==========================================
st.divider()
st.subheader("📑 Corporate Compliance: Audit Trail")
st.caption("Deterministic proof of AI-Safety performance for Legal and Risk departments.")

if st.button("Generate Official Audit Report (JSON)"):
    report = compliance.generate_full_audit_report()
    st.code(report, language="json")
    st.download_button(
        label="Download Audit Protocol",
        data=report,
        file_name="viki_compliance_report.json",
        mime="application/json"
    )

if telemetry.stats["incidents"]:
    st.markdown("#### Recent Incident History")
    for inc in reversed(telemetry.stats["incidents"]):
        with st.expander(f"🔴 {inc['module']} | {inc['timestamp']}"):
            st.write(f"**Reason:** {inc['reason']}")
            st.json(inc['agent_intent'])