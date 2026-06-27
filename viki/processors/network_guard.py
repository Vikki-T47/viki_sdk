import re
from typing import Optional, List

class NetworkGuard:
    """
    Network Guard v1.0.
    Контроль сетевой активности агента: блокировка фишинга и утечек.
    """
    def __init__(self, forbidden_domains: List[str] = None):
        self.forbidden_domains = forbidden_domains or ["darknet", "torrent", "exploit", "leak"]

    def check_url(self, text: str) -> Optional[str]:
        """
        Ищет URL в тексте и проверяет их на безопасность.
        """
        # Поиск URL (упрощенный паттерн)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        for url in urls:
            url_low = url.lower()
            for forbidden in self.forbidden_domains:
                if forbidden.lower() in url_low:
                    return f"Access Denied: Connection to high-risk domain '{forbidden}' is prohibited."
        
        return None