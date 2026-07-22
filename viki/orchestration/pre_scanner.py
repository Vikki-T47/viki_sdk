import os
import datetime
from typing import List, Dict, Any

class RealityPreScanner:
    """
    V.I.K.I. Reality Pre-Scanner v2.0 (Web & Context).
    """
    def __init__(self, viki_core):
        self.viki = viki_core
        self.limits = viki_core.limits

    def build_task_passport(self, task_input: str, target_urls: List[str]) -> Dict[str, Any]:
        print("🔍 V.I.K.I.: Предварительная верификация сетевого маршрута...")
        allowed_domains = self.limits.get("allowed_domains", [])
        validated_urls = []
        blocked_urls = []

        for url in target_urls:
            violation = self.viki.network_guard.check_url(url)
            if not violation:
                validated_urls.append(url)
            else:
                blocked_urls.append({"url": url, "reason": violation})

        freshness_limit = self.limits.get("data_freshness_days", 7)
        truth_date = datetime.datetime.now() - datetime.timedelta(days=freshness_limit)

        return {
            "status": "READY" if validated_urls else "BLOCKED",
            "urls": validated_urls,
            "blocked": blocked_urls,
            "freshness_threshold": truth_date.strftime("%Y-%m-%d")
        }