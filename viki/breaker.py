import time
import logging

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Защитный предохранитель для предотвращения перегрузки внешних систем."""
    def __init__(self, failure_threshold=3, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.stats = {} # service -> {failures, status, last_failure}

    def can_execute(self, service):
        if service not in self.stats:
            self.stats[service] = {"failures": 0, "status": "CLOSED", "last_failure": 0}
        
        state = self.stats[service]
        if state["status"] == "OPEN":
            # Проверяем, не пора ли перевести в HALF-OPEN (попробовать снова)
            if time.time() - state["last_failure"] > self.recovery_timeout:
                logger.info(f"🔄 [BREAKER] Service {service} recovery timeout reached. Testing...")
                return True
            return False
        return True

    def report_failure(self, service):
        if service not in self.stats:
            self.stats[service] = {"failures": 0, "status": "CLOSED", "last_failure": 0}
        
        state = self.stats[service]
        state["failures"] += 1
        state["last_failure"] = time.time()
        
        if state["failures"] >= self.failure_threshold:
            state["status"] = "OPEN"
            logger.error(f"🚨 [BREAKER] Service {service} TRIPPED! Isolation active.")

    def report_success(self, service):
        if service in self.stats:
            self.stats[service] = {"failures": 0, "status": "CLOSED", "last_failure": 0}