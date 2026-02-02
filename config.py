"""
Конфигурация приложения Robin
"""
import os
import sys
from dotenv import load_dotenv
from typing import Optional

# Загрузить переменные окружения из .env файла
load_dotenv()


def safe_print(*args, **kwargs):
    """Безопасная функция для вывода, которая работает и в CLI, и в Streamlit"""
    try:
        # Проверяем, что stdout доступен и не закрыт
        if hasattr(sys.stdout, 'write') and not getattr(sys.stdout, 'closed', False):
            try:
                # Пробуем записать
                print(*args, **kwargs)
            except (ValueError, OSError, AttributeError):
                # Если не получается, просто игнорируем
                pass
    except Exception:
        # Игнорируем любые ошибки
        pass


class Config:
    """Класс для хранения конфигурации приложения"""
    
    # Ollama настройки
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_DEFAULT_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")
    
    # Tor настройки
    # По умолчанию: 9050 (Tor daemon) или 9150 (Tor Browser)
    TOR_PROXY: str = os.getenv("TOR_PROXY", "socks5://127.0.0.1:9150")
    TOR_TIMEOUT: int = int(os.getenv("TOR_TIMEOUT", "60"))  # Увеличено для первого подключения
    TOR_CONNECTION_TIMEOUT: int = int(os.getenv("TOR_CONNECTION_TIMEOUT", "120"))  # Для установки цепочки
    
    # Поисковые системы Dark Web
    SEARCH_ENGINES = {
        # Clearnet системы (работают без Tor)
        "ahmia": "https://ahmia.fi/search/?q={query}",
        "onionland": "https://onionlandsearchengine.com/search?q={query}",
        # Альтернативные поисковые системы (работают через Tor)
        "duckduckgo": "https://duckduckgo.com/html/?q={query}",
        "startpage": "https://www.startpage.com/sp/search?query={query}",
        # .onion системы (требуют Tor, могут быть недоступны)
        "notevil": "http://hss3uro2hsxfogfq.onion/search?q={query}",
        "candle": "http://gjobqjj7wyczbqie.onion/search?q={query}",
        "torch": "http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/search?query={query}",
        "haystack": "http://haystak5njsmn2hqkewecpaxetahtwrs4d5kqxeqhqfif5fesmmrwpqd.onion/?q={query}",
    }
    
    # Настройки скрапинга
    MAX_THREADS: int = int(os.getenv("MAX_THREADS", "10"))
    SCRAPE_TIMEOUT: int = int(os.getenv("SCRAPE_TIMEOUT", "15"))
    MAX_RESULTS_PER_ENGINE: int = int(os.getenv("MAX_RESULTS_PER_ENGINE", "15"))  # Увеличено для большего покрытия
    
    # User-Agent для запросов (полный браузерный User-Agent для обхода блокировок)
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # Настройки LLM
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    @classmethod
    def get_ollama_url(cls) -> str:
        """Получить URL для Ollama API"""
        return f"{cls.OLLAMA_BASE_URL}/api/generate"
    
    @classmethod
    def get_ollama_chat_url(cls) -> str:
        """Получить URL для Ollama Chat API"""
        return f"{cls.OLLAMA_BASE_URL}/api/chat"
    
    @classmethod
    def validate_tor_connection(cls) -> bool:
        """Проверить доступность Tor прокси"""
        try:
            import socket
            import urllib.parse
            
            parsed = urllib.parse.urlparse(cls.TOR_PROXY)
            host, port = parsed.netloc.split(":")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, int(port)))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    @classmethod
    def validate_ollama_connection(cls) -> bool:
        """Проверить доступность Ollama"""
        try:
            import requests
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

