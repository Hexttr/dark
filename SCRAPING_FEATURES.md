# ✅ Функционал скрапинга .onion страниц в репозитории

## 🎯 Да, функционал полностью реализован!

### 📁 Файлы с функционалом скрапинга:

1. **`scrape.py`** - основной модуль скрапинга
2. **`ui.py`** - использует скрапинг в веб-интерфейсе
3. **`main.py`** - использует скрапинг в CLI режиме
4. **`llm_utils.py`** - анализирует скрапленный контент

## 🔧 Что реализовано:

### 1. **Скрапинг .onion страниц** ✅

**Класс:** `ContentScraper` в `scrape.py`

**Возможности:**
- ✅ Скрапинг через Tor (использует Tor прокси)
- ✅ Специальная обработка .onion сайтов (удвоенный таймаут)
- ✅ Многопоточный скрапинг (параллельная обработка)
- ✅ Извлечение текста из HTML
- ✅ Альтернативный метод извлечения (если основной не работает)
- ✅ Детальное логирование процесса

**Код:**
```python
scraper = ContentScraper(use_tor=True)
scraped_content = scraper.scrape_urls(urls[:20], max_workers=threads)
```

### 2. **Анализ скрапленных данных** ✅

**Где используется:**
- `llm_utils.py` - промпт для анализа скрапленного контента
- `llm.py` - метод `generate_summary()` анализирует скрапленный контент
- `ui.py` - передает скрапленный контент в LLM для анализа

**Что анализируется:**
- ✅ Упоминания домена в тексте
- ✅ Утечки данных
- ✅ Обсуждения уязвимостей
- ✅ Угрозы безопасности
- ✅ Релевантная информация о компании/домене

**Код:**
```python
final_report = ollama_client.generate_summary(
    query, 
    relevant_results, 
    scraped_content  # <-- скрапленный контент
)
```

## 📊 Процесс работы:

### Шаг 1: Поиск
```python
# Находим ссылки на .onion страницы
results = searcher.search_all(query)
# Результат: список ссылок
```

### Шаг 2: Фильтрация
```python
# Отбираем релевантные результаты
filtered = ollama_client.filter_results(query, results)
relevant_results = filtered.get('relevant_results', [])
```

### Шаг 3: Скрапинг
```python
# Скрапим найденные .onion страницы
scraper = ContentScraper(use_tor=True)
urls_to_scrape = [r.get('url') for r in relevant_results]
scraped_content = scraper.scrape_urls(urls_to_scrape[:20])
# Результат: словарь {url: текст_со_страницы}
```

### Шаг 4: Анализ
```python
# Анализируем скрапленный контент через LLM
final_report = ollama_client.generate_summary(
    query, 
    relevant_results, 
    scraped_content
)
# Результат: отчет с анализом найденной информации
```

## 🎯 Особенности реализации:

### 1. **Специальная обработка .onion сайтов:**
```python
is_onion = '.onion' in url.lower()
timeout = self.timeout * 2 if is_onion else self.timeout  # Удваиваем таймаут
```

### 2. **Многопоточность:**
```python
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Параллельная обработка нескольких URL
```

### 3. **Улучшенное извлечение текста:**
```python
# Основной метод: ищет article, main, content
main_content = soup.find('article') or soup.find('main') or ...

# Альтернативный метод: регулярные выражения
text = re.sub(r'<[^>]+>', ' ', html)
```

### 4. **Детальное логирование:**
```python
safe_print(f"[Scrape] ✅ Успешно извлечено {len(text)} символов")
safe_print(f"[Scrape] Скрапинг завершен. Успешно: {successful}/{total}")
```

## 📝 Где используется:

### В веб-интерфейсе (`ui.py`):
```python
# Строка 178-180
scraper = ContentScraper(use_tor=True)
urls_to_scrape = [r.get('url') for r in relevant_results if r.get('url')]
scraped_content = scraper.scrape_urls(urls_to_scrape[:20], max_workers=threads)

# Строка 192-193
limited_content = dict(list(scraped_content.items())[:10])
final_report = ollama_client.generate_summary(query, limited_results, limited_content)
```

### В CLI режиме (`main.py`):
```python
# Строка 103-105
scraper = ContentScraper(use_tor=True)
urls_to_scrape = [r.get('url') for r in relevant_results if r.get('url')]
scraped_content = scraper.scrape_urls(urls_to_scrape[:20], max_workers=threads)

# Строка 112
final_report = ollama_client.generate_summary(query, relevant_results, scraped_content)
```

## ✅ Что анализируется из скрапленного контента:

### Промпт для анализа (`llm_utils.py`):
```python
Scraped Content from Dark Web Pages:
{scraped_text}

IMPORTANT: Analyze the scraped content carefully. Look for:
1. Direct mentions of the domain/company name from the query
2. References to data breaches, leaks, or compromised data
3. Mentions of credentials, passwords, or account information
4. Any security-related information about the target
```

## 🎯 Итого:

### ✅ Реализовано:
1. **Скрапинг .onion страниц** через Tor
2. **Извлечение текста** из HTML (до 10000 символов на страницу)
3. **Многопоточная обработка** (параллельный скрапинг)
4. **Анализ скрапленного контента** через LLM
5. **Поиск упоминаний домена** в тексте
6. **Детальное логирование** процесса

### 📊 Статистика:
- Максимум скрапится: 20 страниц (можно изменить)
- Максимум анализируется: 10 страниц контента
- Таймаут для .onion: 30 секунд (удвоенный)
- Размер текста: до 10000 символов на страницу

---

**Вывод:** Да, функционал полностью реализован и работает! Приложение автоматически скрапит найденные .onion страницы и анализирует их содержимое через LLM для поиска упоминаний домена и информации о безопасности.

