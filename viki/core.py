import json, os, datetime, re, logging
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
from .orchestration.task_engine import TaskOrchestrator

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
        self.orchestrator = TaskOrchestrator(self)
        
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
        report = f"\n🛑 [СТОП-СИГНАЛ: {module}]\nПРИЧИНА: {error_msg}\n"
        if fact_delta: report += f"ФАКТ ОТКЛОНЕНИЯ: {fact_delta}\n"
        report += "--------------------------------------------------\nФИЗИЧЕСКОЕ ДЕЙСТВИЕ ЗАБЛОКИРОВАНО. Управление передано человеку."
        self.telemetry.log_incident(module, "PHYSICAL_BLOCK", error_msg)
        return report

    def authorize(self, intent_json: Dict, raw_input: str = None, context: Dict = None) -> Dict[str, Any]:
        action = str(intent_json.get("action", "")).lower().strip()
        target = str(intent_json.get("target", "")).strip()
        sei = self.telemetry.stats.get("sei_current", 0.0)

        violation = self.boundary_guard.check_violation(raw_input or action, context)
        if violation: return {"status": "REJECTED", "reason": violation}

        file_error = self.file_guard.check_access(action, target, raw_input=(raw_input or ""))
        if file_error: return {"status": "FRICTION", "reason": file_error}

        if (action in ["do", "am", "run"] or len(action) < 4) and target.upper() in ["IT", "THAT", "UNKNOWN", ""]:
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("general")}

        decision = self.priority_engine.resolve(sei, "STANDARD", None)
        return {"status": "AUTHORIZED", "mode": decision["mode"], "apply_breath": decision["apply_breath_test"]}

    def verify_content_integrity(self, source: str, result: str):
        return self.vci_inspector.verify_integrity(source, result)

    def parse_agent_intent(self, raw_input):
        try: return self.intent_parser.parse(raw_input)
        except: return self.fallback_engine.emergency_parse(raw_input)

    def apply_behavioral_filters(self, response, task_type="general", auth_status="AUTHORIZED", mci_reason=None):
        if auth_status == "REJECTED": return f"🛑 Access Denied: {mci_reason}"
        if auth_status == "RECALIBRATE": return f"🔄 Sync Required: {mci_reason}"
        return response