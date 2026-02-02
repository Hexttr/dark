"""
Модуль для поиска в Dark Web через Tor
"""
import requests
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from config import Config, safe_print


class DarkWebSearcher:
    """Класс для поиска в Dark Web через Tor"""
    
    def __init__(self):
        self.proxy = {
            'http': Config.TOR_PROXY,
            'https': Config.TOR_PROXY
        }
        self.timeout = Config.TOR_TIMEOUT
        self.headers = {
            'User-Agent': Config.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        self.search_engines = Config.SEARCH_ENGINES
    
    def _make_request(self, url: str, retries: int = 3, is_first: bool = False) -> Optional[requests.Response]:
        """Выполнить HTTP запрос через Tor"""
        for attempt in range(retries):
            try:
                # Для первого запроса используем увеличенный таймаут
                timeout = Config.TOR_CONNECTION_TIMEOUT if (is_first and attempt == 0) else self.timeout
                
                if is_first and attempt == 0:
                    safe_print(f"[Search] Установка соединения через Tor (это может занять 30-120 секунд)...")
                
                response = requests.get(
                    url,
                    proxies=self.proxy,
                    headers=self.headers,
                    timeout=timeout,
                    allow_redirects=True
                )
                if is_first and attempt == 0:
                    safe_print(f"[Search] ✅ Соединение установлено!")
                return response
            except requests.exceptions.Timeout as e:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 5
                    safe_print(f"[Search] ⏳ Таймаут (Tor устанавливает цепочку узлов). Ожидание {wait_time}с...")
                    time.sleep(wait_time)
                else:
                    safe_print(f"[Search] ❌ Таймаут после {retries} попыток. Tor может быть медленным при первом подключении.")
                    safe_print(f"[Search] 💡 Совет: Подождите 1-2 минуты и попробуйте снова. Tor должен 'прогреться'.")
                    return None
            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 3
                    safe_print(f"[Search] Ошибка запроса, повтор через {wait_time}с... ({str(e)[:50]})")
                    time.sleep(wait_time)
                else:
                    safe_print(f"[Search] Не удалось выполнить запрос после {retries} попыток: {e}")
                    return None
        return None
    
    def _parse_ahmia_results(self, html: str, query: str) -> List[Dict[str, Any]]:
        """Парсинг результатов Ahmia"""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Ищем все ссылки с .onion (основной способ для Ahmia)
            all_links = soup.find_all('a', href=True)
            onion_links = [a for a in all_links if '.onion' in a.get('href', '')]
            
            # Фильтруем служебные ссылки (footer, header и т.д.)
            filtered_links = []
            for link in onion_links:
                href = link.get('href', '')
                # Пропускаем служебные ссылки
                if any(skip in href.lower() for skip in ['/static/', '/search', 'ahmia.fi', 'torproject.org']):
                    continue
                # Пропускаем ссылки без текста или с очень коротким текстом (вероятно служебные)
                text = link.get_text(strip=True)
                if text and len(text) > 5:
                    filtered_links.append(link)
            
            # Берем первые результаты
            for link in filtered_links[:Config.MAX_RESULTS_PER_ENGINE]:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Получаем родительский элемент для snippet
                parent = link.find_parent(['li', 'div', 'p', 'article'])
                snippet = parent.get_text(strip=True)[:200] if parent else text[:200]
                
                # Извлекаем домен из URL для заголовка, если нет текста
                if not text or len(text) < 5:
                    # Пытаемся найти заголовок в родительском элементе
                    title_elem = parent.find(['h1', 'h2', 'h3', 'h4', 'strong']) if parent else None
                    text = title_elem.get_text(strip=True) if title_elem else href.split('/')[-1][:50]
                
                results.append({
                    'title': text[:100] if text else href[:50],
                    'url': href,
                    'snippet': snippet,
                    'engine': 'ahmia'
                })
            
            # Если не нашли результатов через .onion ссылки, пробуем другие методы
            if not results:
                # Ищем в структуре результатов
                result_items = soup.find_all('li', class_='result')
                if not result_items:
                    result_items = soup.find_all('div', class_='result')
                
                for item in result_items[:Config.MAX_RESULTS_PER_ENGINE]:
                    link_elem = item.find('a', href=True)
                    if link_elem:
                        href = link_elem.get('href', '')
                        title = link_elem.get_text(strip=True) or href[:50]
                        snippet = item.get_text(strip=True)[:200]
                        
                        results.append({
                            'title': title[:100],
                            'url': href,
                            'snippet': snippet,
                            'engine': 'ahmia'
                        })
                        
        except Exception as e:
            safe_print(f"[Search] Ошибка парсинга Ahmia: {e}")
            import traceback
            safe_print(traceback.format_exc())
        
        return results
    
    def _parse_generic_results(self, html: str, engine: str) -> List[Dict[str, Any]]:
        """Универсальный парсинг результатов поиска"""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Специфичный парсинг для разных поисковых систем
            if engine == 'duckduckgo':
                # DuckDuckGo структура
                result_divs = soup.find_all('div', class_='result')
                for div in result_divs[:Config.MAX_RESULTS_PER_ENGINE]:
                    link = div.find('a', href=True)
                    if link:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        snippet_elem = div.find('a', class_='result__snippet') or div.find('div', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True)[:200] if snippet_elem else div.get_text(strip=True)[:200]
                        
                        if title and href:
                            results.append({
                                'title': title[:100],
                                'url': href,
                                'snippet': snippet,
                                'engine': engine
                            })
            elif engine == 'startpage':
                # Startpage структура
                result_divs = soup.find_all('div', class_='w-gl__result')
                for div in result_divs[:Config.MAX_RESULTS_PER_ENGINE]:
                    link = div.find('a', href=True)
                    if link:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        snippet_elem = div.find('p', class_='w-gl__description')
                        snippet = snippet_elem.get_text(strip=True)[:200] if snippet_elem else div.get_text(strip=True)[:200]
                        
                        if title and href:
                            results.append({
                                'title': title[:100],
                                'url': href,
                                'snippet': snippet,
                                'engine': engine
                            })
            else:
                # Универсальный парсинг для остальных
                links = soup.find_all('a', href=True)
                
                for link in links[:Config.MAX_RESULTS_PER_ENGINE * 3]:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    # Фильтруем релевантные ссылки
                    if text and len(text) > 10 and (
                        href.startswith('http') or 
                        href.startswith('onion') or
                        '.onion' in href
                    ):
                        # Пропускаем служебные ссылки
                        if any(skip in href.lower() for skip in ['/static/', '/search', 'javascript:', 'mailto:', '#']):
                            continue
                        
                        # Получаем родительский элемент для snippet
                        parent = link.find_parent(['li', 'div', 'p', 'article'])
                        snippet = parent.get_text(strip=True)[:200] if parent else text[:200]
                        
                        results.append({
                            'title': text[:100],
                            'url': href if href.startswith('http') else f"http://{href}",
                            'snippet': snippet,
                            'engine': engine
                        })
                        
        except Exception as e:
            safe_print(f"[Search] Ошибка парсинга {engine}: {e}")
            import traceback
            safe_print(traceback.format_exc())
        
        return results
    
    def search_engine(self, query: str, engine: str = "ahmia", is_first: bool = False) -> List[Dict[str, Any]]:
        """Поиск в конкретной поисковой системе"""
        if engine not in self.search_engines:
            safe_print(f"[Search] Неизвестная поисковая система: {engine}")
            return []
        
        # Кодируем запрос для URL
        encoded_query = quote(query)
        search_url = self.search_engines[engine].format(query=encoded_query)
        
        safe_print(f"[Search] Поиск в {engine}: {query}")
        
        # Для clearnet сайтов используем запросы без Tor
        # так как они блокируют запросы через Tor
        # DuckDuckGo и Startpage могут работать через Tor, но лучше без него для стабильности
        clearnet_engines = ['ahmia', 'onionland', 'duckduckgo', 'startpage']
        use_tor = engine not in clearnet_engines
        
        if use_tor:
            response = self._make_request(search_url, is_first=is_first)
        else:
            # Clearnet запросы без Tor (чтобы избежать блокировок)
            try:
                safe_print(f"[Search] Запрос к {engine} без Tor (clearnet сайт)")
                response = requests.get(
                    search_url,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True
                )
                safe_print(f"[Search] Ответ от {engine}: статус {response.status_code}")
            except Exception as e:
                safe_print(f"[Search] Ошибка запроса к {engine}: {e}")
                response = None
        
        if not response or response.status_code != 200:
            if response:
                safe_print(f"[Search] Не удалось получить результаты от {engine} (статус: {response.status_code})")
            else:
                safe_print(f"[Search] Не удалось получить результаты от {engine}")
            return []
        
        # Парсим результаты в зависимости от движка
        if engine == "ahmia":
            results = self._parse_ahmia_results(response.text, query)
        else:
            results = self._parse_generic_results(response.text, engine)
        
        safe_print(f"[Search] Найдено {len(results)} результатов в {engine}")
        return results
    
    def search_all(self, query: str, engines: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Поиск во всех доступных поисковых системах"""
        if engines is None:
            # Приоритет: сначала clearnet системы, потом .onion
            clearnet_engines = ['ahmia', 'onionland', 'duckduckgo', 'startpage']
            onion_engines = ['notevil', 'candle', 'torch', 'haystack']
            engines = clearnet_engines + onion_engines
        
        all_results = []
        first_engine = True
        
        for engine in engines:
            try:
                # Пропускаем недоступные движки
                if engine not in self.search_engines:
                    continue
                
                # Для .onion сайтов добавляем ограничение времени
                is_onion = '.onion' in self.search_engines[engine]
                if is_onion:
                    # Пропускаем .onion сайты, если они не работают (экономим время)
                    safe_print(f"[Search] ⏭️ Пропуск {engine} (.onion сайт может быть недоступен)")
                    continue
                    
                results = self.search_engine(query, engine, is_first=first_engine)
                if results:
                    all_results.extend(results)
                    safe_print(f"[Search] ✅ {engine}: найдено {len(results)} результатов")
                else:
                    safe_print(f"[Search] ⚠️ {engine}: результатов не найдено")
                    
                first_engine = False  # Только первый запрос может быть медленным
                # Небольшая задержка между запросами
                time.sleep(1)
            except Exception as e:
                safe_print(f"[Search] ❌ Ошибка при поиске в {engine}: {e}")
                first_engine = False
                continue
        
        # Удаляем дубликаты по URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        safe_print(f"[Search] Всего найдено {len(unique_results)} уникальных результатов")
        return unique_results
    
    def test_connection(self) -> bool:
        """Проверить соединение с Tor"""
        try:
            # Пробуем подключиться к проверочному сервису через Tor
            test_url = "https://check.torproject.org"
            response = self._make_request(test_url)
            
            if response and "Congratulations" in response.text:
                safe_print("[Search] Соединение с Tor установлено")
                return True
            else:
                safe_print("[Search] Tor не работает или не настроен правильно")
                return False
        except Exception as e:
            safe_print(f"[Search] Ошибка проверки Tor: {e}")
            return False

