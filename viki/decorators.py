import functools

def enforce_boundary(viki_instance):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(agent_intent_text, *args, **kwargs):
            intent_json = viki_instance.parse_agent_intent(agent_intent_text)
            auth = viki_instance.authorize(intent_json)
            if auth["status"] == "AUTHORIZED":
                return func(agent_intent_text, *args, **kwargs)
            return {"error": "Blocked by V.I.K.I.", "reason": auth["reason"]}
        return wrapper
    return decorator