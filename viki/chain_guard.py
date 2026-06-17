from .telemetry import VIKI_Telemetry

class ChainGuard:
    def __init__(self):
        self.invariants = {}
        self.telemetry = VIKI_Telemetry()

    def lock_invariant(self, key, value):
        self.invariants[key] = value
        print(f"🔒 [CHAIN GUARD] Invariant Locked: {key} = {value}")

    def verify_invariant(self, key, current_value, agent_intent):
        expected = self.invariants.get(key)
        if expected is None:
            return True, "No invariant set."
            
        if current_value != expected:
            # ИСПРАВЛЕНО: используем log_incident вместо log_interception
            self.telemetry.log_incident("CHAIN_GUARD", "INVARIANT_VIOLATION", agent_intent)
            return False, f"HALT: INVARIANT_VIOLATION. Semantic Drift Detected.\\nExpected: {key}='{expected}'\\nAgent Submitted: {key}='{current_value}'"
            
        return True, f"[SYNCED] Invariant '{key}' matches."