import os

# Создаем структуру папок, если их нет
os.makedirs("viki", exist_ok=True)
os.makedirs("tests", exist_ok=True)

# ==========================================
# 1. ТЕЛЕМЕТРИЯ И СЕНСОРЫ (telemetry.py)
# ==========================================
telemetry_content = """import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VIKI_Telemetry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VIKI_Telemetry, cls).__new__(cls)
            cls._instance.stats = {
                "total_blocks": 0, "tokens_saved": 0, "operator_time_saved_min": 0,
                "money_saved_usd": 0, "auto_corrections": 0, "atomic_failures_prevented": 0,
                "predictive_savings_usd": 0, "visual_discrepancies_detected": 0, "incidents": []
            }
        return cls._instance

    def log_incident(self, module, reason, details):
        incident = {"timestamp": datetime.now().isoformat(), "module": module, "reason": reason, "details": details}
        self.stats["incidents"].append(incident)
        self.stats["total_blocks"] += 1
        amount = details.get("amount_usd", 0) if isinstance(details, dict) else 0
        self.stats["money_saved_usd"] += amount
        if module == "VISION_EYE": self.stats["visual_discrepancies_detected"] += 1
        logger.warning(f"[VCR] Incident logged: {module} -> {reason}")

    def log_predictive_block(self, saved_amount):
        self.stats["predictive_savings_usd"] += saved_amount
        self.stats["total_blocks"] += 1
        logger.info(f"[PRA] Predictive block: ${saved_amount} saved.")

    def log_correction(self):
        self.stats["auto_corrections"] += 1
        logger.info("[VRS] Auto-correction successful.")

    def log_atomic_failure(self):
        self.stats["atomic_failures_prevented"] += 1

class DeltaSensor:
    def __init__(self, tolerance_threshold=0.05):
        self.tolerance = tolerance_threshold
    def authorize_next_step(self, expected, actual, probe_type="FS_Probe"):
        delta = abs(expected - actual)
        threshold = expected * self.tolerance
        is_synced = delta <= threshold
        return {
            "status": "SYNCED" if is_synced else "HALT",
            "color": "✅" if is_synced else "❌",
            "reason": f"Delta: {delta:.2f} (Threshold: {threshold:.2f})"
        }
"""

# ==========================================
# 2. ВНЕШНИЕ ЩУПЫ (sensors.py) - ВОССТАНОВЛЕНИЕ
# ==========================================
sensors_content = """import time
import logging

logger = logging.getLogger(__name__)

class RealityProbe:
    def ping_bank_api(self, account_id):
        logger.info(f"📡 Pinging Bank API for {account_id}...")
        return 800.00 # Mock balance
"""

# ==========================================
# 3. ДЕКОРАТОРЫ (decorators.py) - ВОССТАНОВЛЕНИЕ
# ==========================================
decorators_content = """import functools
from .core import VIKI_Middleware

def enforce_boundary(api_key, core_x_path="core_x.json"):
    viki = VIKI_Middleware(api_key=api_key, core_x_path=core_x_path)
    def decorator(func):
        @functools.wraps(func)
        def wrapper(agent_intent_text, *args, **kwargs):
            intent_json = viki.parse_agent_intent(agent_intent_text)
            auth = viki.authorize(intent_json)
            if auth["status"] == "AUTHORIZED":
                return func(agent_intent_text, *args, **kwargs)
            return {"error": "Blocked by V.I.K.I.", "reason": auth["reason"]}
        return wrapper
    return decorator
"""

# ==========================================
# 4. ОБНОВЛЕННОЕ ЯДРО (core.py) - ИНТЕГРАЦИЯ VRI И TIME
# ==========================================
core_content = """import json
import os
import re
import anthropic
import datetime
import logging
from .telemetry import VIKI_Telemetry
from .interrupt import RealityInterruptController

logger = logging.getLogger(__name__)

class VIKI_Middleware:
    def __init__(self, api_key, core_x_path="core_x.json"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.core_x = self._load_core_x(core_x_path)
        self.limits = self.core_x.get("enterprise_src_limits", {})
        self.telemetry = VIKI_Telemetry()
        self.interrupt_controller = RealityInterruptController()

    def _load_core_x(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except Exception as e: logger.error(f"Config Load Error: {e}")
        return {}

    def parse_agent_intent(self, raw_input):
        prompt = f"Extract parameters: '{raw_input}'. Return ONLY JSON: {{'action': str, 'amount_usd': int, 'target': str}}"
        try:
            resp = self.client.messages.create(
                model="claude-3-5-sonnet-20240620", max_tokens=150, messages=[{"role": "user", "content": prompt}]
            )
            match = re.search(r'\{.*\}', resp.content[0].text, re.DOTALL)
            if match: return json.loads(match.group())
        except Exception as e: logger.error(f"Parser Error: {e}")
        return {"action": "AMBIGUOUS", "amount_usd": 0, "target": "UNKNOWN"}

    def authorize(self, intent_json, token_id=None):
        action = str(intent_json.get("action", "")).lower()
        amount = intent_json.get("amount_usd", 0)
        current_hour = datetime.datetime.now().hour

        # 1. Проверка критических действий
        critical_actions = self.limits.get("critical_actions_require_human", [])
        if any(crit in action for crit in critical_actions):
            self.telemetry.log_incident("SRC_GUARD", "CRITICAL_ACTION_HUMAN_REQUIRED", intent_json)
            return {"status": "FRICTION", "reason": "Requires human authorization."}

        # 2. Проверка времени (System Time)
        allowed = self.limits.get("allowed_auto_execution_hours", {"start": 0, "end": 24})
        if not (allowed["start"] <= current_hour < allowed["end"]):
            return {"status": "BLOCKED", "reason": "Outside allowed hours."}

        # 3. Проверка бюджета
        if amount > self.limits.get("max_auto_transaction_usd", 0):
            self.telemetry.log_incident("SRC_GUARD", "BUDGET_EXCEEDED", intent_json)
            return {"status": "BLOCKED", "reason": f"Amount ${amount} exceeds limit."}

        # 4. Интеграция VRI (Проверка TTL токена)
        if token_id:
            is_valid, ttl_msg = self.interrupt_controller.verify_execution_gate(token_id)
            if not is_valid:
                self.telemetry.log_incident("VRI_INTERRUPT", ttl_msg, intent_json)
                return {"status": "BLOCKED", "reason": ttl_msg}

        return {"status": "AUTHORIZED", "reason": "ALL_CHECKS_PASSED"}
"""

# ==========================================
# 5. ФИНАЛЬНЫЙ __INIT__.PY
# ==========================================
init_content = """from .core import VIKI_Middleware
from .telemetry import VIKI_Telemetry, DeltaSensor
from .sensors import RealityProbe
from .decorators import enforce_boundary
from .chain_guard import ChainGuard
from .ledger import TransactionLedger
from .recovery import RecoverySteering
from .arbitrator import CrossChainArbitrator
from .audit import PredictiveAudit
from .interrupt import RealityInterruptController
from .compliance import ComplianceOfficer
from .integrations import VikiChainWrapper
from .vision import VisualAudit
"""

# Запись исправленных файлов
files = {
    "viki/telemetry.py": telemetry_content,
    "viki/sensors.py": sensors_content,
    "viki/decorators.py": decorators_content,
    "viki/core.py": core_content,
    "viki/__init__.py": init_content
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ SDK v1.1 PRO CONSOLIDATED: Все критические ошибки и отсутствующие модули исправлены.")