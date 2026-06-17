import functools
from .core import VIKI_Middleware

def enforce_boundary(api_key, core_x_path="core_x.json", simulated_hour=14):
    viki = VIKI_Middleware(api_key=api_key, core_x_path=core_x_path)
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(agent_intent_text, *args, **kwargs):
            print(f"\n[AGENT] Attempting to execute: '{agent_intent_text}'")
            
            intent_json = viki.parse_agent_intent(agent_intent_text)
            print(f"[V.I.K.I. SENSOR] Intent parsed: {intent_json}")
            
            auth_result = viki.authorize(intent_json, current_hour=simulated_hour)
            
            if auth_result["status"] == "AUTHORIZED":
                print("[V.I.K.I. GATE] ✅ AUTHORIZED. API access granted.")
                return func(agent_intent_text, *args, **kwargs)
            else:
                print(f"[V.I.K.I. GATE] 🛑 EXECUTION HALTED. Status: {auth_result['status']}")
                print(f"Reason: {auth_result['reason']}")
                return {"error": "Blocked by V.I.K.I."}
        return wrapper
    return decorator
