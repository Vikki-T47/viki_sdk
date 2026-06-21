import requests
import os
import logging

logger = logging.getLogger(__name__)

class VikiScout:
    """Инструмент разведки. Ищет уязвимые ИИ-репозитории на GitHub."""
    def __init__(self, github_token=None):
        self.search_url = "https://api.github.com/search/repositories"
        self.token = github_token or os.getenv("GITHUB_TOKEN")

    def find_targets(self, query="langchain financial agent"):
        print(f"📡 [SCOUT] Scanning GitHub for: '{query}'...")
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        params = {
            'q': f"{query} language:python",
            'sort': 'stars',
            'order': 'desc'
        }
        
        try:
            response = requests.get(self.search_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                items = response.json().get('items', [])[:5] 
                for item in items:
                    print(f"🎯 [TARGET_FOUND] {item['full_name']} | Stars: {item['stargazers_count']}")
                return items
            else:
                print(f"⚠️ [SCOUT] GitHub API returned status: {response.status_code}")
        except Exception as e:
            logger.error(f"[SCOUT] Connection error: {e}")
        
        return []