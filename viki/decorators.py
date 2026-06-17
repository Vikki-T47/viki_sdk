import functools
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
