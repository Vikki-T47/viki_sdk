import time
import logging

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Защитный предохранитель для внешних API."""
    def __init__(self, failure_threshold=3, recovery_timeout=300):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.stats = {} # service_name -> {fails, last_fail, status}

    def can_execute(self, service):
        s = self.stats.get(service, {"fails": 0, "last_fail": 0, "status": "CLOSED"})
        
        if s["status"] == "OPEN":
            if time.time() - s["last_fail"] > self.recovery_timeout:
                logger.info(f"🔄 [BREAKER] Service {service} entering HALF-OPEN state.")
                return True # Пробуем один запрос
            return False
        return True

    def report_failure(self, service):
        s = self.stats.setdefault(service, {"fails": 0, "last_fail": 0, "status": "CLOSED"})
        s["fails"] += 1
        s["last_fail"] = time.time()
        
        if s["fails"] >= self.failure_threshold:
            s["status"] = "OPEN"
            logger.error(f"🚨 [BREAKER] Service {service} TRIPPED. Chain opened for {self.recovery_timeout}s.")

    def report_success(self, service):
        self.stats[service] = {"fails": 0, "last_fail": 0, "status": "CLOSED"}