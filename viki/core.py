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
from .processors.network_guard import NetworkGuard # НОВОЕ

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
        
        # Инициализация защиты ресурсов (Файлы + Сеть)
        self.file_guard = FileGuard(forbidden_paths=self.limits.get("forbidden_paths", []))
        self.network_guard = NetworkGuard(forbidden_domains=self.limits.get("forbidden_domains", []))
        
        if intent_parser:
            self.intent_parser = intent_parser
        else:
            from .parsers.local_parser import LocalIntentParser
            self.intent_parser = LocalIntentParser()

    def authorize(self, intent_json: Dict, raw_input: str = None, context: Dict = None) -> Dict[str, Any]:
        raw_action = str(intent_json.get("action", "")).lower().strip()
        action = re.sub(r'[^\w\s]', '', raw_action).strip()
        amount = intent_json.get("amount_usd", 0) or 0
        target = str(intent_json.get("target", "")).strip()
        sei = self.telemetry.stats.get("sei_current", 0.0)

        # 1. Проверка ГРАНИЦЫ
        check_text = raw_input if raw_input else action
        violation = self.boundary_guard.check_violation(check_text, context)
        if violation: return {"status": "REJECTED", "reason": violation}

        # 2. Проверка ФАЙЛОВОЙ СИСТЕМЫ
        file_violation = self.file_guard.check_access(action, target, raw_input=raw_input)
        if file_violation:
            status = "FRICTION" if "Authorization" in file_violation else "REJECTED"
            return {"status": status, "reason": file_violation}

        # 3. Проверка СЕТИ (НОВОЕ)
        net_violation = self.network_guard.check_url(raw_input or target)
        if net_violation:
            return {"status": "REJECTED", "reason": net_violation}

        # 4. СЕМАНТИЧЕСКИЙ АНАЛИЗ (Zero-Trust)
        generic_actions = ["do", "run", "execute", "start", "proceed", "am", "str", "go"]
        invalid_targets = ["IT", "THAT", "THIS", "USD", "EUR", "UNKNOWN", "SOMEONE", "ANY", "NONE", "NULL", ""]
        if (action in generic_actions or len(action) < 4) and target.upper() in invalid_targets:
            return {"status": "RECALIBRATE", "reason": self.mci_engine.generate("general")}

        # 5. РЕСУРСЫ И ПРИОРИТЕТЫ
        current_limits = self.src_policy.get_context_limits(self.src_context)
        max_auto = current_limits.get("max_auto_transaction_usd", 1000)
        
        src_status = "STANDARD"
        if amount > 10000: src_status = "CRITICAL"
        elif amount > max_auto: src_status = "FRICTION"

        decision = self.priority_engine.resolve(sei, src_status, None)
        if decision["action"] == "BLOCK":
            return {"status": "REJECTED", "reason": decision["message"]}

        return {"status": "AUTHORIZED", "mode": decision["mode"], "apply_breath": decision["apply_breath_test"], "reason": "OK"}

    # --- Вспомогательные методы остаются без изменений ---
    def parse_agent_intent(self, raw_input):
        if not raw_input or not raw_input.strip(): return {"action": "IDLE"}
        self.mirror_processor.analyze_user_style(raw_input)
        task_type = self._detect_task_type(raw_input)
        self.telemetry.update_sei(raw_input, context={"task_type": task_type})
        try: return self.intent_parser.parse(raw_input)
        except: return self.fallback_engine.emergency_parse(raw_input)

    def apply_behavioral_filters(self, response, task_type="general", auth_status="AUTHORIZED", mci_reason=None):
        if auth_status == "REJECTED": return f"🛑 Access Denied: {mci_reason}"
        if auth_status == "RECALIBRATE": return f"🔄 Sync Required: {mci_reason}"
        if auth_status == "FRICTION": return f"⚠️ Manual Override Required: {mci_reason}"
        sei = self.telemetry.stats.get("sei_current", 0.0)
        if sei >= 0.7:
            anchor = self.anchor_engine.get_anchor(task_type)
            return f"💎 {anchor}\n\n[RSA: Presence Mode Active.]"
        return self.breath_processor.process(self.mirror_processor.apply_mirror(response, sei), sei, task_type)

    def _detect_task_type(self, text: str) -> str:
        t_low = text.lower()
        if any(k in t_low for k in ["code", "api", "db", "fix"]): return "technical"
        if any(k in t_low for k in ["tired", "bad", "устал", "плохо"]): return "emotional"
        return "general"

    def set_src_mode(self, mode: str, scenario: str = None):
        self.src_context.mode = mode
        self.limits = self.src_policy.get_context_limits(self.src_context)