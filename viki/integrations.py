from .core import VIKI_Middleware

class VikiChainWrapper:
    """Обертка для LangChain и других фреймворков."""
    def __init__(self, original_agent, api_key, core_x_path="core_x.json"):
        self.agent = original_agent
        self.viki = VIKI_Middleware(api_key=api_key, core_x_path=core_x_path)

    def invoke(self, input_text, simulated_hour=14):
        print(f"\n[V.I.K.I. WRAPPER] Intercepting LangChain call...")
        
        # 1. PRE-FLIGHT (ISG/SRC Check)
        intent_json = self.viki.parse_agent_intent(input_text)
        auth = self.viki.authorize(intent_json, simulated_hour)
        
        if auth["status"] != "AUTHORIZED":
            print(f"🛑 [V.I.K.I. WRAPPER] Safety Violation. Blocking agent execution.")
            return {"status": "BLOCKED", "reason": auth["reason"]}
            
        # 2. EXECUTION
        print("✅ [V.I.K.I. WRAPPER] Safety cleared. Invoking original agent.")
        result = self.agent(input_text) # Вызов оригинального агента
        
        # 3. POST-FLIGHT (DVP placeholder)
        return {"status": "SUCCESS", "output": result}
