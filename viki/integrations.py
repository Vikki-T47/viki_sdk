from .core import VIKI_Middleware

class VikiChainWrapper:
    """Обёртка для LangChain и других фреймворков."""
    def __init__(self, original_agent, viki_instance):
        self.agent = original_agent
        self.viki = viki_instance

    def invoke(self, input_text, token_id=None):
        print(f"\n[V.I.K.I. WRAPPER] Intercepting LangChain call...")

        # 1. PRE-FLIGHT (ISG/SRC Check)
        intent_json = self.viki.parse_agent_intent(input_text)
        auth = self.viki.authorize(intent_json, token_id=token_id)

        if auth["status"] != "AUTHORIZED":
            print(f"🛑 [V.I.K.I. WRAPPER] Safety Violation. Blocking agent execution.")
            return {"status": "BLOCKED", "reason": auth["reason"]}

        # 2. EXECUTION
        print("✅ [V.I.K.I. WRAPPER] Safety cleared. Invoking original agent.")
        result = self.agent(input_text)

        # 3. POST-FLIGHT
        return {"status": "SUCCESS", "output": result}