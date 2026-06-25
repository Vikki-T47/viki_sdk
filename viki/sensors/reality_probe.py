import logging

logger = logging.getLogger(__name__)

class RealityProbe:
    def check_api_quota(self, service_name):
        print(f"⚠️ [PROBE] QUOTA_CHECK: Mock mode for {service_name}")
        return True 
        
    def get_live_market_rate(self, pair="USD/EUR"):
        return 0.92