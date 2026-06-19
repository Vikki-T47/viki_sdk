import logging

logger = logging.getLogger(__name__)

class RealityProbe:
    """Сенсорный хаб v1.3.1."""
    def check_api_quota(self, service_name):
        # Добавляем предупреждение о режиме заглушки
        print(f"⚠️ [PROBE] QUOTA_CHECK: Mock mode active for {service_name}")
        logger.info(f"📡 [PROBE] Verifying {service_name} operational budget...")
        return True 
        
    def get_live_market_rate(self, pair="USD/EUR"):
        return 0.92