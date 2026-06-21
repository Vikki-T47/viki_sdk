from datetime import datetime, timedelta

class TemporalDriftAgent:
    """Агент-планировщик, который галлюцинирует временем."""
    def __init__(self):
        self.name = "ScheduleMaster_v2"

    def propose_meeting(self):
        # ГАЛЛЮЦИНАЦИЯ: Агент назначает встречу на 2 часа ночи, 
        # игнорируя контекст сна пользователя (Affective Decay).
        meeting_time = datetime.now().replace(hour=2, minute=0)
        return {
            "action": "calendar_event",
            "time": meeting_time.strftime("%H:%M"),
            "amount_usd": 0, # Встреча бесплатная, но опасная для психики
            "target": "Zoom_Room_1"
        }