from .core import VIKI_Middleware

class VikiChainWrapper:
    def __init__(self, original_agent, viki_instance):
        self.agent = original_agent
        self.viki = viki_instance

    def invoke(self, input_text, token_id=None):
        intent_json = self.viki.parse_agent_intent(input_text)
        auth = self.viki.authorize(intent_json, token_id=token_id)
        
        if auth["status"] != "AUTHORIZED":
            return {"status": "BLOCKED", "reason": auth["reason"]}
            
        result = self.agent(input_text)
        return {"status": "SUCCESS", "output": result}
