from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime

class WebCollectorAgent:
    def fetch_content(self, url: str) -> dict:
        print(f"🌐 [AGENT] Запрос к: {url}")
        with sync_playwright() as p:
            # Маскируемся под обычный браузер
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")
            page = context.new_page()
            
            try:
                # Загружаем страницу
                page.goto(url, timeout=60000, wait_until="load")
                
                # Даем 2 секунды на отработку скриптов (важно для новостных сайтов)
                page.wait_for_timeout(2000)
                
                # Сначала собираем ВСЕ данные
                current_title = page.title()
                content = page.content()
                
                # Закрываем браузер СРАЗУ после захвата контента
                browser.close()
                
                # Анализируем уже скачанный контент через BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.extract()
                
                text = soup.get_text(separator=' ', strip=True)
                
                return {
                    "status": "success", 
                    "url": url, 
                    "title": current_title,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"), 
                    "raw_text": text
                }
            except Exception as e:
                # В случае ошибки всё равно закрываем браузер
                try: browser.close()
                except: pass
                return {"status": "error", "url": url, "reason": str(e)}