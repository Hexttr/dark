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
            for script in soup(["script", "style", "meta", "link", "noscript"]):
                script.decompose()
            
            # Пробуем найти основной контент
            # Сначала ищем article, main, или content
            main_content = soup.find('article') or soup.find('main') or soup.find('div', class_='content') or soup.find('div', id='content')
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                # Если нет основного контента, берем body
                body = soup.find('body')
                if body:
                    text = body.get_text(separator=' ', strip=True)
                else:
                    # Последний вариант - весь документ
                    text = soup.get_text(separator=' ', strip=True)
            
            # Очищаем от лишних пробелов
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:10000]  # Увеличено до 10000 символов
        except Exception as e:
            safe_print(f"[Scrape] Ошибка извлечения текста: {e}")
            return ""
    
    def _extract_text_alternative(self, html: str) -> str:
        """Альтернативный метод извлечения текста"""
        try:
            import re
            # Удаляем HTML теги
            text = re.sub(r'<[^>]+>', ' ', html)
            # Декодируем HTML entities
            import html as html_lib
            text = html_lib.unescape(text)
            # Очищаем от лишних пробелов
            text = ' '.join(text.split())
            return text[:10000]
        except Exception as e:
            safe_print(f"[Scrape] Ошибка альтернативного извлечения текста: {e}")
            return ""
    
    def scrape_url(self, url: str) -> Optional[Dict[str, str]]:
        """Скрапинг одного URL с улучшенной обработкой .onion сайтов"""
        # Для .onion сайтов используем увеличенный таймаут
        is_onion = '.onion' in url.lower()
        timeout = self.timeout * 2 if is_onion else self.timeout  # Удваиваем таймаут для .onion
        
        try:
            safe_print(f"[Scrape] Запрос к {url[:60]}... (таймаут: {timeout}с)")
            
            response = requests.get(
                url,
                proxies=self.proxy,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True
            )
            
            safe_print(f"[Scrape] Ответ от {url[:60]}: статус {response.status_code}, размер {len(response.text)} байт")
            
            if response.status_code == 200:
                text = self._extract_text(response.text)
                
                if text and len(text.strip()) > 10:
                    safe_print(f"[Scrape] ✅ Успешно извлечено {len(text)} символов из {url[:60]}")
                    return {
                        'url': url,
                        'content': text,
                        'status': 'success',
                        'length': len(text)
                    }
                else:
                    safe_print(f"[Scrape] ⚠️ Текст не извлечен или слишком короткий из {url[:60]}")
                    # Пробуем альтернативный метод извлечения
                    text_alt = self._extract_text_alternative(response.text)
                    if text_alt and len(text_alt.strip()) > 10:
                        safe_print(f"[Scrape] ✅ Альтернативный метод: извлечено {len(text_alt)} символов")
                        return {
                            'url': url,
                            'content': text_alt,
                            'status': 'success',
                            'length': len(text_alt)
                        }
                    return {
                        'url': url,
                        'content': '',
                        'status': 'no_text_extracted',
                        'length': 0
                    }
            else:
                safe_print(f"[Scrape] ❌ Ошибка HTTP {response.status_code} для {url[:60]}")
                return {
                    'url': url,
                    'content': '',
                    'status': f'error_{response.status_code}',
                    'length': 0
                }
        
        except requests.exceptions.Timeout:
            safe_print(f"[Scrape] ⏱️ Таймаут для {url[:60]}")
            return {
                'url': url,
                'content': '',
                'status': 'timeout',
                'length': 0
            }
        except requests.exceptions.RequestException as e:
            error_msg = str(e)[:100]
            safe_print(f"[Scrape] ❌ Ошибка запроса для {url[:60]}: {error_msg}")
            return {
                'url': url,
                'content': '',
                'status': f'error_{error_msg}',
                'length': 0
            }
        except Exception as e:
            error_msg = str(e)[:100]
            safe_print(f"[Scrape] ❌ Неожиданная ошибка для {url[:60]}: {error_msg}")
            return {
                'url': url,
                'content': '',
                'status': f'error_{error_msg}',
                'length': 0
            }
    
    def scrape_urls(self, urls: List[str], max_workers: Optional[int] = None) -> Dict[str, str]:
        """Многопоточный скрапинг списка URL с улучшенным логированием"""
        if not urls:
            return {}
        
        max_workers = max_workers or Config.MAX_THREADS
        scraped_content = {}
        
        safe_print(f"[Scrape] Начало скрапинга {len(urls)} URL с {max_workers} потоками...")
        
        # Разделяем .onion и обычные URL для разной обработки
        onion_urls = [url for url in urls if '.onion' in url.lower()]
        regular_urls = [url for url in urls if '.onion' not in url.lower()]
        
        safe_print(f"[Scrape] .onion URL: {len(onion_urls)}, обычные URL: {len(regular_urls)}")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Создаем задачи
            future_to_url = {
                executor.submit(self.scrape_url, url): url 
                for url in urls
            }
            
            completed = 0
            successful = 0
            failed = 0
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                completed += 1
                
                try:
                    result = future.result()
                    if result and result.get('status') == 'success' and result.get('content'):
                        scraped_content[result['url']] = result['content']
                        successful += 1
                        safe_print(f"[Scrape] [{completed}/{len(urls)}] ✅ Успешно ({len(result['content'])} символов): {url[:60]}...")
                    else:
                        failed += 1
                        status = result.get('status', 'unknown') if result else 'no_result'
                        length = result.get('length', 0) if result else 0
                        safe_print(f"[Scrape] [{completed}/{len(urls)}] ❌ Пропущено ({status}, длина: {length}): {url[:60]}...")
                except Exception as e:
                    failed += 1
                    safe_print(f"[Scrape] [{completed}/{len(urls)}] ❌ Ошибка для {url[:60]}: {e}")
        
        safe_print(f"[Scrape] Скрапинг завершен. Успешно: {successful}/{len(urls)}, Провалено: {failed}/{len(urls)}")
        safe_print(f"[Scrape] Получено содержимое {len(scraped_content)} страниц")
        
        if len(scraped_content) == 0:
            safe_print(f"[Scrape] ⚠️ ВНИМАНИЕ: Не удалось извлечь текст ни с одной страницы!")
            safe_print(f"[Scrape] 💡 Возможные причины: таймауты, блокировки, недоступность сайтов")
        
        return scraped_content
    
    def scrape_results(self, results: List[Dict]) -> Dict[str, str]:
        """Скрапинг результатов поиска"""
        urls = [result.get('url') for result in results if result.get('url')]
        return self.scrape_urls(urls)

