import json
import os
from typing import Dict, Any, Optional

class SRCContext:
    def __init__(self, mode: str = "production", scenario: Optional[str] = None):
        self.mode = mode
        self.scenario = scenario
        self.error_count = 0 

class SRCPolicyEngine:
    def __init__(self, core_x_path: str = "core_x.json"):
        self.core_x_path = core_x_path
        self.refresh()

    def _load_config(self) -> Dict:
        if os.path.exists(self.core_x_path):
            with open(self.core_x_path, "r", encoding="utf-8") as f:
                try: return json.load(f)
                except: return {}
        return {}

    def refresh(self):
        config = self._load_config()
        self.base_limits = config.get("enterprise_src_limits", {})
        self.context_policies = config.get("context_policies", {})
        self.dynamic_rules = config.get("dynamic_rules", {})

    def get_context_limits(self, context: SRCContext) -> Dict[str, Any]:
        # Сначала берем базу
        policy = self.base_limits.copy()
        
        # Накладываем специфику мода (например, 5000 для simulation)
        mode_policy = self.context_policies.get(context.mode, {})
        for key, value in mode_policy.items():
            policy[key] = value

        if context.scenario:
            scenario_policy = self.context_policies.get(context.scenario, {})
            for key, value in scenario_policy.items():
                policy[key] = value

        # Динамический штраф
        if self.dynamic_rules.get("reduce_after_error", False) and context.error_count > 0:
            penalty = (self.dynamic_rules.get("error_reduction_percent", 15) / 100) * context.error_count
            if "max_auto_transaction_usd" in policy:
                # Лимит не может упасть ниже 10% от номинала
                policy["max_auto_transaction_usd"] *= max(0.1, (1 - penalty))
        
        return policy