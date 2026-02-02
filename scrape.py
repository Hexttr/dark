"""
Модуль для скрапинга контента с найденных URL
"""
import requests
import time
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from config import Config, safe_print


class ContentScraper:
    """Класс для скрапинга контента с веб-страниц"""
    
    def __init__(self, use_tor: bool = True):
        self.use_tor = use_tor
        self.proxy = {
            'http': Config.TOR_PROXY,
            'https': Config.TOR_PROXY
        } if use_tor else None
        self.timeout = Config.SCRAPE_TIMEOUT
        self.headers = {
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def _extract_text(self, html: str) -> str:
        """Извлечь текст из HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Удаляем скрипты и стили
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            # Получаем текст
            text = soup.get_text(separator=' ', strip=True)
            
            # Очищаем от лишних пробелов
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Ограничиваем размер
        except Exception as e:
            safe_print(f"[Scrape] Ошибка извлечения текста: {e}")
            return ""
    
    def scrape_url(self, url: str) -> Optional[Dict[str, str]]:
        """Скрапинг одного URL"""
        try:
            response = requests.get(
                url,
                proxies=self.proxy,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                text = self._extract_text(response.text)
                return {
                    'url': url,
                    'content': text,
                    'status': 'success',
                    'length': len(text)
                }
            else:
                return {
                    'url': url,
                    'content': '',
                    'status': f'error_{response.status_code}',
                    'length': 0
                }
        
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'content': '',
                'status': 'timeout',
                'length': 0
            }
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'content': '',
                'status': f'error_{str(e)[:50]}',
                'length': 0
            }
        except Exception as e:
            return {
                'url': url,
                'content': '',
                'status': f'error_{str(e)[:50]}',
                'length': 0
            }
    
    def scrape_urls(self, urls: List[str], max_workers: Optional[int] = None) -> Dict[str, str]:
        """Многопоточный скрапинг списка URL"""
        if not urls:
            return {}
        
        max_workers = max_workers or Config.MAX_THREADS
        scraped_content = {}
        
        safe_print(f"[Scrape] Начало скрапинга {len(urls)} URL с {max_workers} потоками...")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Создаем задачи
            future_to_url = {
                executor.submit(self.scrape_url, url): url 
                for url in urls
            }
            
            completed = 0
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                completed += 1
                
                try:
                    result = future.result()
                    if result and result.get('status') == 'success':
                        scraped_content[result['url']] = result['content']
                        safe_print(f"[Scrape] [{completed}/{len(urls)}] Успешно: {url[:60]}...")
                    else:
                        status = result.get('status', 'unknown') if result else 'no_result'
                        safe_print(f"[Scrape] [{completed}/{len(urls)}] Пропущено ({status}): {url[:60]}...")
                except Exception as e:
                    safe_print(f"[Scrape] [{completed}/{len(urls)}] Ошибка для {url[:60]}: {e}")
        
        safe_print(f"[Scrape] Скрапинг завершен. Получено {len(scraped_content)} страниц")
        return scraped_content
    
    def scrape_results(self, results: List[Dict]) -> Dict[str, str]:
        """Скрапинг результатов поиска"""
        urls = [result.get('url') for result in results if result.get('url')]
        return self.scrape_urls(urls)

