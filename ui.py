"""
Веб-интерфейс Robin на Streamlit - исправленная версия
"""
import sys
import os

# Исправление кодировки для Windows (только если не запущено через Streamlit)
if sys.platform == 'win32':
    try:
        import io
        # Проверяем, что stdout не закрыт и доступен для записи
        if hasattr(sys.stdout, 'buffer') and not sys.stdout.closed:
            try:
                # Пробуем записать, чтобы проверить доступность
                sys.stdout.write('')
                sys.stdout.flush()
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            except (ValueError, AttributeError, OSError):
                # Если не получается, просто пропускаем - Streamlit сам управляет кодировкой
                pass
        if hasattr(sys.stderr, 'buffer') and not sys.stderr.closed:
            try:
                sys.stderr.write('')
                sys.stderr.flush()
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
            except (ValueError, AttributeError, OSError):
                pass
    except Exception:
        # Игнорируем любые ошибки при настройке кодировки
        pass

import streamlit as st
from datetime import datetime

# Безопасный импорт с обработкой ошибок
try:
    from config import Config
except Exception as e:
    st.error(f"Ошибка импорта Config: {e}")
    st.stop()

try:
    from llm import OllamaClient
except Exception as e:
    st.error(f"Ошибка импорта OllamaClient: {e}")
    st.stop()

try:
    from search import DarkWebSearcher
except Exception as e:
    st.error(f"Ошибка импорта DarkWebSearcher: {e}")
    st.stop()

try:
    from scrape import ContentScraper
except Exception as e:
    st.error(f"Ошибка импорта ContentScraper: {e}")
    st.stop()


def check_connections():
    """Проверка соединений с обработкой ошибок"""
    try:
        tor_ok = Config.validate_tor_connection()
    except Exception as e:
        st.warning(f"Ошибка проверки Tor: {e}")
        tor_ok = False
    
    try:
        ollama_ok = Config.validate_ollama_connection()
    except Exception as e:
        st.warning(f"Ошибка проверки Ollama: {e}")
        ollama_ok = False
    
    return tor_ok, ollama_ok


def run_investigation_ui(query: str, model: str, threads: int):
    """Запуск расследования в UI режиме"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.container()
    
    try:
        # Проверка соединений
        status_text.text("Проверка соединений...")
        progress_bar.progress(10)
        
        tor_ok, ollama_ok = check_connections()
        if not tor_ok:
            progress_bar.progress(100)
            status_text.text("❌ Ошибка")
            st.error("❌ Tor не доступен! Убедитесь, что Tor запущен.")
            return None
        if not ollama_ok:
            progress_bar.progress(100)
            status_text.text("❌ Ошибка")
            st.error(f"❌ Ollama не доступен! Убедитесь, что Ollama запущен на {Config.OLLAMA_BASE_URL}")
            return None
        
        # Генерация запросов
        status_text.text("Генерация поисковых запросов...")
        progress_bar.progress(20)
        
        try:
            ollama_client = OllamaClient(model=model)
            search_queries = ollama_client.generate_search_queries(query)
        except Exception as e:
            st.error(f"Ошибка генерации запросов: {e}")
            search_queries = [query]  # Используем оригинальный запрос
        
        with results_container:
            st.success(f"✅ Сгенерировано {len(search_queries)} поисковых запросов")
            with st.expander("Просмотр запросов"):
                for i, q in enumerate(search_queries, 1):
                    st.write(f"{i}. {q}")
        
        # Поиск
        status_text.text("Поиск в Dark Web...")
        progress_bar.progress(40)
        
        try:
            searcher = DarkWebSearcher()
            all_results = []
            
            # Ограничиваем количество запросов для ускорения
            max_queries = min(len(search_queries), 5)  # Максимум 5 запросов
            
            for i, search_query in enumerate(search_queries[:max_queries], 1):
                status_text.text(f"Поиск в Dark Web... ({i}/{max_queries})")
                progress_bar.progress(40 + int(30 * i / max_queries))
                
                try:
                    results = searcher.search_all(search_query)
                    all_results.extend(results)
                except Exception as e:
                    st.warning(f"Ошибка поиска для запроса '{search_query}': {e}")
                    continue
        except Exception as e:
            st.error(f"Ошибка поиска: {e}")
            all_results = []
        
        if not all_results:
            progress_bar.progress(100)
            status_text.text("✅ Поиск завершен")
            st.warning("Результаты не найдены")
            return {
                'report': f"# Отчет расследования\n\n**Запрос:** {query}\n**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n## Результаты\n\nРезультаты поиска не найдены. Попробуйте изменить запрос или проверить соединение с Tor.",
                'results': [],
                'total_found': 0,
                'relevant_count': 0
            }
        
        with results_container:
            st.success(f"✅ Найдено {len(all_results)} результатов")
        
        # Фильтрация
        status_text.text("Фильтрация результатов...")
        progress_bar.progress(60)
        
        try:
            # Ограничиваем количество результатов для фильтрации (ускоряет работу)
            results_to_filter = all_results[:50]  # Максимум 50 результатов для фильтрации
            filtered = ollama_client.filter_results(query, results_to_filter)
            relevant_results = filtered.get('relevant_results', [])
        except Exception as e:
            st.warning(f"Ошибка фильтрации: {e}")
            relevant_results = all_results[:10]  # Берем первые 10
        
        with results_container:
            st.success(f"✅ Отфильтровано {len(relevant_results)} релевантных результатов")
        
        # Скрапинг
        status_text.text("Скрапинг контента...")
        progress_bar.progress(80)
        
        try:
            scraper = ContentScraper(use_tor=True)
            urls_to_scrape = [r.get('url') for r in relevant_results if r.get('url')]
            scraped_content = scraper.scrape_urls(urls_to_scrape[:20], max_workers=threads)
        except Exception as e:
            st.warning(f"Ошибка скрапинга: {e}")
            scraped_content = {}
        
        # Генерация отчета
        status_text.text("Генерация отчета...")
        progress_bar.progress(90)
        
        try:
            # Ограничиваем данные для генерации отчета (ускоряет работу)
            limited_results = relevant_results[:20]  # Максимум 20 результатов
            limited_content = dict(list(scraped_content.items())[:10])  # Максимум 10 страниц контента
            final_report = ollama_client.generate_summary(query, limited_results, limited_content)
        except Exception as e:
            st.warning(f"Ошибка генерации отчета: {e}")
            final_report = f"""
# Отчет расследования

**Запрос:** {query}
**Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Найденные результаты

Всего найдено: {len(all_results)}
Релевантных: {len(relevant_results)}

## Релевантные результаты:

{chr(10).join([f"- {r.get('title', 'N/A')}: {r.get('url', 'N/A')}" for r in relevant_results[:10]])}
"""
        
        progress_bar.progress(100)
        status_text.text("✅ Готово!")
        
        return {
            'report': final_report,
            'results': relevant_results,
            'total_found': len(all_results),
            'relevant_count': len(relevant_results)
        }
    
    except Exception as e:
        progress_bar.progress(100)
        status_text.text("❌ Ошибка")
        st.error(f"Критическая ошибка: {e}")
        import traceback
        with st.expander("Детали ошибки"):
            st.code(traceback.format_exc())
        return None


def main():
    """Главная функция UI"""
    try:
        st.set_page_config(
            page_title="Robin - Dark Web OSINT",
            page_icon="🕵️",
            layout="wide"
        )
    except Exception:
        pass  # Уже настроено
    
    st.title("🕵️ Robin - AI-Powered Dark Web OSINT Tool")
    st.markdown("---")
    
    # Проверка соединений
    try:
        tor_ok, ollama_ok = check_connections()
    except Exception as e:
        st.error(f"Ошибка проверки соединений: {e}")
        tor_ok, ollama_ok = False, False
    
    # Боковая панель с настройками
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # Проверка соединений
        st.subheader("Статус соединений")
        
        if tor_ok:
            st.success("✅ Tor подключен")
        else:
            st.error("❌ Tor не доступен")
        
        if ollama_ok:
            st.success("✅ Ollama подключен")
        else:
            st.error("❌ Ollama не доступен")
        
        st.markdown("---")
        
        # Настройки модели
        try:
            ollama_client = OllamaClient()
            available_models = ollama_client.list_models()
            
            if available_models:
                selected_model = st.selectbox(
                    "Модель Ollama",
                    options=available_models,
                    index=0
                )
            else:
                selected_model = st.text_input(
                    "Модель Ollama",
                    value=Config.OLLAMA_DEFAULT_MODEL
                )
        except Exception as e:
            st.warning(f"Не удалось загрузить список моделей: {e}")
            selected_model = st.text_input(
                "Модель Ollama",
                value=Config.OLLAMA_DEFAULT_MODEL
            )
        
        threads = st.slider(
            "Количество потоков",
            min_value=1,
            max_value=20,
            value=10,
            help="Количество параллельных потоков для скрапинга"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Информация")
        st.info("""
        **Robin** использует AI для:
        - Генерации оптимизированных поисковых запросов
        - Фильтрации результатов поиска
        - Создания итоговых отчетов
        
        Все данные обрабатываются локально через Ollama.
        """)
    
    # Основная форма
    st.header("🔍 Расследование")
    
    # Информационная панель с примерами
    with st.expander("💡 Как правильно использовать приложение?", expanded=False):
        st.markdown("""
        **❌ Неправильно:** Вводить URL напрямую (например: `https://example.com`)
        
        **✅ Правильно:** Вводить поисковые запросы на английском языке:
        - `password leak database 2024`
        - `data breach company-name customer data`
        - `email credentials leak your-email@example.com`
        - `ransomware payments victims 2024`
        - `phishing campaigns banking fake login`
        
        **Как это работает:**
        1. Вы вводите ключевые слова для поиска
        2. AI генерирует оптимизированные запросы
        3. Приложение ищет в dark web поисковых системах
        4. Результаты фильтруются и анализируются
        5. Создается итоговый отчет
        
        **Примеры правильных запросов:**
        - Проверка утечек: `email password leak database dump`
        - Мониторинг компании: `company-name data breach ransomware`
        - Поиск угроз: `zero-day vulnerability exploit 2024`
        - Исследование фишинга: `phishing campaign fake website banking`
        """)
    
    query = st.text_area(
        "Поисковый запрос",
        placeholder="Введите ключевые слова для поиска (на английском)...\nПримеры:\n- password leak database 2024\n- data breach company-name\n- email credentials leak your-email@example.com",
        height=100,
        help="⚠️ ВАЖНО: Вводите ключевые слова, а не URL! Приложение ищет информацию в dark web по вашему запросу."
    )
    
    # Автоматическое преобразование URL в поисковый запрос
    if query and (query.startswith('http://') or query.startswith('https://') or query.startswith('www.')):
        # Извлекаем домен из URL
        domain = query.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]
        query = f"domain {domain} credentials leak data breach vulnerability"
        st.info(f"ℹ️ URL автоматически преобразован в поисковый запрос для кибербезопасности: `{query}`")
    
    # Если это просто домен, автоматически добавляем контекст кибербезопасности
    if query and '.' in query and len(query.split()) == 1 and not query.startswith('http'):
        st.info("ℹ️ Домен обнаружен. Приложение автоматически сгенерирует запросы для поиска утечек данных, уязвимостей и обсуждений атак.")
    
    # Кнопка по центру и шире
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_button = st.button("🚀 Запустить расследование", type="primary", use_container_width=True)
    
    if run_button:
        if not query:
            st.warning("Пожалуйста, введите поисковый запрос")
        elif not tor_ok or not ollama_ok:
            st.error("Пожалуйста, убедитесь, что Tor и Ollama запущены")
            # Повторная проверка
            tor_ok, ollama_ok = check_connections()
        else:
            # Автоматическое преобразование URL в поисковый запрос
            processed_query = query.strip()
            
            # Если это URL, извлекаем домен
            if processed_query.startswith('http://') or processed_query.startswith('https://') or processed_query.startswith('www.'):
                domain = processed_query.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]
                processed_query = domain
                st.info(f"ℹ️ URL автоматически преобразован в домен: `{domain}`")
            
            # Если это просто домен, показываем информационное сообщение
            if '.' in processed_query and len(processed_query.split()) == 1:
                st.info("ℹ️ Домен обнаружен. Приложение автоматически сгенерирует запросы для поиска утечек данных, уязвимостей и обсуждений атак.")
            if processed_query.startswith('http://') or processed_query.startswith('https://') or processed_query.startswith('www.'):
                # Извлекаем домен из URL
                from urllib.parse import urlparse
                try:
                    if not processed_query.startswith('http'):
                        processed_query = 'https://' + processed_query
                    parsed = urlparse(processed_query)
                    domain = parsed.netloc or parsed.path.split('/')[0]
                    domain = domain.replace('www.', '')
                    # Преобразуем в поисковый запрос
                    processed_query = f"domain {domain} credentials leak data breach"
                    st.info(f"🔄 URL преобразован в поисковый запрос: `{processed_query}`")
                except Exception:
                    # Если не удалось распарсить, используем как есть
                    pass
            
            with st.spinner("Выполняется расследование... Это может занять несколько минут."):
                result = run_investigation_ui(processed_query, selected_model, threads)
                
                if result:
                    st.markdown("---")
                    st.header("📊 Результаты расследования")
                    
                    # Статистика
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Всего найдено", result['total_found'])
                    with col2:
                        st.metric("Релевантных", result['relevant_count'])
                    with col3:
                        st.metric("Скраплено страниц", len([r for r in result['results'] if r.get('url')]))
                    
                    # Отчет
                    st.subheader("📄 Итоговый отчет")
                    st.markdown(result['report'])
                    
                    # Источники
                    with st.expander("📚 Источники"):
                        for i, r in enumerate(result['results'], 1):
                            st.markdown(f"**{i}. {r.get('title', 'N/A')}**")
                            st.markdown(f"URL: `{r.get('url', 'N/A')}`")
                            if r.get('key_findings'):
                                st.markdown(f"Находки: {r.get('key_findings')}")
                            st.markdown("---")
                    
                    # Скачивание отчета
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    report_text = f"""Robin - AI-Powered Dark Web OSINT Report
{'='*60}

Запрос: {query}
Модель: {selected_model}
Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Найдено результатов: {result['total_found']}
Релевантных: {result['relevant_count']}

{'='*60}

{result['report']}

{'='*60}
Источники:
{chr(10).join([f"- {r.get('title', 'N/A')}: {r.get('url', 'N/A')}" for r in result['results']])}
"""
                    
                    st.download_button(
                        label="💾 Скачать отчет",
                        data=report_text,
                        file_name=f"robin_report_{timestamp}.txt",
                        mime="text/plain"
                    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("Критическая ошибка при загрузке интерфейса")
        st.code(str(e))
        import traceback
        with st.expander("Детали ошибки"):
            st.code(traceback.format_exc())
        st.info("Попробуйте перезагрузить страницу (F5)")

