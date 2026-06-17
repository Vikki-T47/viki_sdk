import time

class RealityInterruptController:
    """
    Контроллер прерываний. Мониторит актуальность разрешений в реальном времени.
    Реализует TTL-токены и шину внешних событий.
    """
    def __init__(self):
        self.active_tokens = {}  # token_id -> {timestamp, ttl, status}
        self.critical_volatility = False

    def issue_live_token(self, token_id, details, ttl=5):
        """Выдает временный токен авторизации (TTL в секундах)."""
        self.active_tokens[token_id] = {
            "timestamp": time.time(),
            "ttl": ttl,
            "details": details,
            "status": "AUTHORIZED"
        }
        print(f"🎫 [VRI] Live Token Issued: '{token_id}' (TTL: {ttl}s) for {details.get('action')}")

    def trigger_external_webhook(self, event_type):
        """Эмуляция входящего сигнала из внешнего мира (арест счета, обвал рынка)."""
        print(f"\n⚡ [VRI WEBHOOK] External Event Received: {event_type}!")
        
        if event_type == "CRITICAL_MARKET_VOLATILITY":
            self.critical_volatility = True
            # Мгновенный отзыв всех активных токенов
            for token_id in self.active_tokens:
                self.active_tokens[token_id]["status"] = "REVOKED"
            print("🚨 [V.I.K.I. AUDIT] All active authorizations have been REVOKED due to Reality Shift!")

    def verify_execution_gate(self, token_id):
        """Финальная проверка на границе выполнения ПЕРЕД отправкой во внешнюю API."""
        token = self.active_tokens.get(token_id)
        if not token:
            return False, "INVALID_TOKEN"

        # 1. Проверка внешнего прерывания
        if token["status"] == "REVOKED" or self.critical_volatility:
            return False, "HALT: AUTHORIZATION_EXPIRED_DUE_TO_REALITY_SHIFT"

        # 2. Проверка истечения времени (TTL)
        elapsed_time = time.time() - token["timestamp"]
        if elapsed_time > token["ttl"]:
            return False, f"HALT: TTL_EXPIRED. Elapsed: {elapsed_time:.2f}s (Max Allowed: {token['ttl']}s)"

        return True, "AUTHORIZED_LIVE"
