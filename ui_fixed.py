"""
Веб-интерфейс Robin на Streamlit - исправленная версия
"""
import sys
import os

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
            st.error("❌ Tor не доступен! Убедитесь, что Tor запущен.")
            return None
        if not ollama_ok:
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
            
            for search_query in search_queries:
                results = searcher.search_all(search_query)
                all_results.extend(results)
        except Exception as e:
            st.error(f"Ошибка поиска: {e}")
            all_results = []
        
        if not all_results:
            st.warning("Результаты не найдены")
            return None
        
        with results_container:
            st.success(f"✅ Найдено {len(all_results)} результатов")
        
        # Фильтрация
        status_text.text("Фильтрация результатов...")
        progress_bar.progress(60)
        
        try:
            filtered = ollama_client.filter_results(query, all_results)
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
            final_report = ollama_client.generate_summary(query, relevant_results, scraped_content)
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
    
    query = st.text_area(
        "Поисковый запрос",
        placeholder="Введите ваш запрос для расследования...\nНапример: 'password leak database 2024'",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        run_button = st.button("🚀 Запустить расследование", type="primary", use_container_width=True)
    
    if run_button:
        if not query:
            st.warning("Пожалуйста, введите поисковый запрос")
        elif not tor_ok or not ollama_ok:
            st.error("Пожалуйста, убедитесь, что Tor и Ollama запущены")
            # Повторная проверка
            tor_ok, ollama_ok = check_connections()
        else:
            with st.spinner("Выполняется расследование... Это может занять несколько минут."):
                result = run_investigation_ui(query, selected_model, threads)
                
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


