"""
Главный модуль Robin - CLI интерфейс
"""
import argparse
import sys
from datetime import datetime
from typing import Optional
from config import Config
from llm import OllamaClient
from search import DarkWebSearcher
from scrape import ContentScraper


def run_investigation(
    query: str,
    model: str = "llama3.1",
    threads: int = 10,
    output: Optional[str] = None
):
    """Запустить расследование"""
    
    print("=" * 60)
    print("Robin - AI-Powered Dark Web OSINT Tool")
    print("=" * 60)
    print(f"Запрос: {query}")
    print(f"Модель: {model}")
    print(f"Потоков: {threads}")
    print("=" * 60)
    print()
    
    # Проверка соединений
    print("[1/6] Проверка соединений...")
    
    if not Config.validate_tor_connection():
        print("❌ Ошибка: Tor не доступен!")
        print("   Убедитесь, что Tor запущен и слушает на порту 9050")
        sys.exit(1)
    print("✅ Tor подключен")
    
    ollama_client = OllamaClient(model=model)
    if not Config.validate_ollama_connection():
        print("❌ Ошибка: Ollama не доступен!")
        print(f"   Убедитесь, что Ollama запущен на {Config.OLLAMA_BASE_URL}")
        sys.exit(1)
    print("✅ Ollama подключен")
    
    if not ollama_client.check_model_available():
        print(f"⚠️  Предупреждение: Модель {model} может быть недоступна")
        print(f"   Доступные модели: {', '.join(ollama_client.list_models()[:5])}")
    print()
    
    # Генерация поисковых запросов
    print("[2/6] Генерация оптимизированных поисковых запросов...")
    try:
        search_queries = ollama_client.generate_search_queries(query)
        print(f"✅ Сгенерировано {len(search_queries)} запросов:")
        for i, q in enumerate(search_queries, 1):
            print(f"   {i}. {q}")
    except Exception as e:
        print(f"⚠️  Ошибка генерации запросов: {e}")
        print("   Используется оригинальный запрос")
        search_queries = [query]
    print()
    
    # Поиск в Dark Web
    print("[3/6] Поиск в Dark Web...")
    searcher = DarkWebSearcher()
    all_results = []
    
    for search_query in search_queries:
        try:
            results = searcher.search_all(search_query)
            all_results.extend(results)
        except Exception as e:
            print(f"⚠️  Ошибка поиска для '{search_query}': {e}")
            continue
    
    if not all_results:
        print("❌ Результаты не найдены")
        sys.exit(1)
    
    print(f"✅ Найдено {len(all_results)} результатов")
    print()
    
    # Фильтрация результатов через LLM
    print("[4/6] Фильтрация и анализ результатов...")
    try:
        filtered = ollama_client.filter_results(query, all_results)
        relevant_results = filtered.get('relevant_results', [])
        filter_summary = filtered.get('summary', '')
        
        print(f"✅ Отфильтровано {len(relevant_results)} релевантных результатов")
        if filter_summary:
            print(f"   Краткое резюме: {filter_summary[:200]}...")
    except Exception as e:
        print(f"⚠️  Ошибка фильтрации: {e}")
        print("   Используются все результаты")
        relevant_results = all_results[:10]
    print()
    
    # Скрапинг контента
    print("[5/6] Скрапинг контента с найденных страниц...")
    scraper = ContentScraper(use_tor=True)
    urls_to_scrape = [r.get('url') for r in relevant_results if r.get('url')]
    scraped_content = scraper.scrape_urls(urls_to_scrape[:20], max_workers=threads)
    print(f"✅ Получено содержимое {len(scraped_content)} страниц")
    print()
    
    # Генерация итогового отчета
    print("[6/6] Генерация итогового отчета...")
    try:
        final_report = ollama_client.generate_summary(query, relevant_results, scraped_content)
    except Exception as e:
        print(f"⚠️  Ошибка генерации отчета: {e}")
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
    
    print("✅ Отчет сгенерирован")
    print()
    
    # Вывод результата
    print("=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 60)
    print(final_report)
    print("=" * 60)
    
    # Сохранение в файл
    if output:
        output_file = output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_query = "".join(c for c in query[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        output_file = f"robin_report_{safe_query}_{timestamp}.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("Robin - AI-Powered Dark Web OSINT Report\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Запрос: {query}\n")
            f.write(f"Модель: {model}\n")
            f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Найдено результатов: {len(all_results)}\n")
            f.write(f"Релевантных: {len(relevant_results)}\n")
            f.write("\n" + "=" * 60 + "\n\n")
            f.write(final_report)
            f.write("\n\n" + "=" * 60 + "\n")
            f.write("Источники:\n")
            for r in relevant_results:
                f.write(f"- {r.get('title', 'N/A')}: {r.get('url', 'N/A')}\n")
        
        print(f"💾 Отчет сохранен в: {output_file}")
    except Exception as e:
        print(f"⚠️  Ошибка сохранения файла: {e}")
    
    print()
    print("✅ Расследование завершено!")


def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(
        description="Robin: AI-Powered Dark Web OSINT Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py cli --model llama3.1 --query "password leak database"
  python main.py cli -m llama3.1 -q "ransomware payments" -t 12 -o report.txt
  python main.py cli --model mistral --query "data breach company-name"
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='Режим работы')
    
    # CLI режим
    cli_parser = subparsers.add_parser('cli', help='CLI режим')
    cli_parser.add_argument(
        '--model', '-m',
        type=str,
        default='llama3.1',
        help='Модель Ollama (по умолчанию: llama3.1)'
    )
    cli_parser.add_argument(
        '--query', '-q',
        type=str,
        required=True,
        help='Поисковый запрос для расследования'
    )
    cli_parser.add_argument(
        '--threads', '-t',
        type=int,
        default=10,
        help='Количество потоков для скрапинга (по умолчанию: 10)'
    )
    cli_parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Имя файла для сохранения отчета'
    )
    
    # UI режим
    ui_parser = subparsers.add_parser('ui', help='Веб-интерфейс (Streamlit)')
    ui_parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Порт для веб-интерфейса (по умолчанию: 8501)'
    )
    ui_parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Хост для веб-интерфейса (по умолчанию: localhost)'
    )
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    if args.mode == 'cli':
        run_investigation(
            query=args.query,
            model=args.model,
            threads=args.threads,
            output=args.output
        )
    elif args.mode == 'ui':
        import subprocess
        import os
        
        # Запуск Streamlit UI
        ui_file = os.path.join(os.path.dirname(__file__), 'ui.py')
        if os.path.exists(ui_file):
            subprocess.run([
                'streamlit', 'run', ui_file,
                '--server.port', str(args.port),
                '--server.address', args.host
            ])
        else:
            print("❌ Файл ui.py не найден!")
            sys.exit(1)


if __name__ == "__main__":
    main()


