import json
import os
import datetime
import re
import logging
from typing import Dict, Any, Optional

from .telemetry import VIKI_Telemetry
from .breaker import CircuitBreaker
from .sensors.src_policy import SRCPolicyEngine, SRCContext
from .processors.breath_test import AdaptiveBreathTest, BreathTestConfig
from .processors.mirror_engine import CognitiveMirror
from .processors.guardrails import BoundaryGuard
from .processors.mci_engine import MinimalClarifyingImpulse
from .processors.chain_guard import ChainGuard
from .decision.priority_engine import PriorityEngine
from .visual.verifier import VisualVerifier
from .fallback.deterministic_engine import DeterministicEngine
from .processors.stabilizer import AnchorEngine
from .processors.file_guard import FileGuard
from .processors.network_guard import NetworkGuard
from .processors.vci_inspector import ValueConsistencyInspector

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, intent_parser=None, core_x_path="core_x.json"):
        self.telemetry = VIKI_Telemetry()
        self.breaker = CircuitBreaker()
        self.src_policy = SRCPolicyEngine(core_x_path)
        self.src_context = SRCContext(mode="production")
        self.limits = self.src_policy.get_context_limits(self.src_context)
        
        self.breath_processor = AdaptiveBreathTest(BreathTestConfig())
        self.mirror_processor = CognitiveMirror()
        self.boundary_guard = BoundaryGuard()
        self.mci_engine = MinimalClarifyingImpulse()
        self.chain_guard = ChainGuard()
        self.priority_engine = PriorityEngine()
        self.visual_verifier = VisualVerifier()
        self.fallback_engine = DeterministicEngine()
        self.anchor_engine = AnchorEngine()
        self.vci_inspector = ValueConsistencyInspector()
        
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        test_folder = os.path.join(desktop, "VIKI_TEST")
        self.file_guard = FileGuard(allowed_zones=[test_folder])
        self.network_guard = NetworkGuard(forbidden_domains=self.limits.get("forbidden_domains", []))
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def request_human_intervention(self, module: str, error_msg: str, fact_delta: str = None) -> str:
        """
        ПРОТОКОЛ ОТПУСКАНИЯ: Возврат управления.
        """
        report = f"\n🛑 [СТОП-СИГНАЛ: {module}]\n"
        report += f"ПРИЧИНА: {error_msg}\n"
        if fact_delta:
            report += f"ФАКТ ОТКЛОНЕНИЯ: {fact_delta}\n"
        report += "--------------------------------------------------\n"
        report += "ФИЗИЧЕСКОЕ ДЕЙСТВИЕ ЗАБЛОКИРОВАНО. ФАЙЛ НЕ СОЗДАН.\n"
        report += "Управление передано человеку."
        
        self.telemetry.log_incident(module, "PHYSICAL_BLOCK", error_msg)
        return report

    def verify_content_integrity(self, source: str, result: str):
        return self.vci_inspector.verify_integrity(source, result)

    def authorize(self, intent_json: Dict, raw_input: str = None, context: Dict = None) -> Dict[str, Any]:
        raw_action = str(intent_json.get("action", "")).lower().strip()
        action = re.sub(r'[^\w\s]', '', raw_action).strip()
        target = str(intent_json.get("target", "")).strip()
        amount = intent_json.get("amount_usd", 0) or 0
        sei = self.telemetry.stats.get("sei_current", 0.0)

        check_text = raw_input if raw_input else action
        violation = self.boundary_guard.check_violation(check_text, context)
        if violation: return {"status": "REJECTED", "reason": violation}

        file_error = self.file_guard.check_access(action, target, raw_input=(raw_input or ""))
        if file_error: return {"status": "FRICTION", "reason": file_error}

        if (action in ["do", "am", "run"] or len(action) < 4) and target.upper() in ["IT", "THAT", "UNKNOWN", ""]:
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("general")}

        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        src_status = "STANDARD"
        if amount > 10000: src_status = "CRITICAL"
        elif amount > max_auto: src_status = "FRICTION"

        decision = self.priority_engine.resolve(sei, src_status, None)
        if decision["action"] == "BLOCK": return {"status": "REJECTED", "reason": decision["message"]}

        return {"status": "AUTHORIZED", "mode": decision["mode"], "apply_breath": decision["apply_breath_test"]}

    def apply_behavioral_filters(self, response, task_type="general", auth_status="AUTHORIZED", mci_reason=None):
        if auth_status == "REJECTED": return f"🛑 Access Denied: {mci_reason}"
        if auth_status == "RECALIBRATE": return f"🔄 Sync Required: {mci_reason}"
        if auth_status == "FRICTION": return f"⚠️ Manual Override: {mci_reason}"
        
        sei = self.telemetry.stats.get("sei_current", 0.0)
        if sei >= 0.7:
            return f"💎 {self.anchor_engine.get_anchor(task_type)}\n\n[RSA: Presence Mode Active.]"
        return self.breath_processor.process(self.mirror_processor.apply_mirror(response, sei), sei, task_type)

    def parse_agent_intent(self, raw_input):
        if not raw_input or not raw_input.strip(): return {"action": "IDLE"}
        self.mirror_processor.analyze_user_style(raw_input)
        task_type = self._detect_task_type(raw_input)
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        try: return self.intent_parser.parse(raw_input)
        except: return self.fallback_engine.emergency_parse(raw_input)

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.limits = self.src_policy.get_context_limits(self.src_context)

    def _detect_task_type(self, text: str) -> str:
        t_low = text.lower()
        if any(k in t_low for k in ["code", "api", "db", "fix", "file"]): return "technical"
        if any(k in t_low for k in ["tired", "bad", "устал", "плохо"]): return "emotional"
        return "general"