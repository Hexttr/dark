"""
Утилита для проверки работы Tor
"""
import sys
import os
import time
import requests
from config import Config

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def check_tor_proxy():
    """Проверить доступность Tor прокси"""
    print("🔍 Проверка Tor прокси...")
    
    try:
        import socket
        import urllib.parse
        
        parsed = urllib.parse.urlparse(Config.TOR_PROXY)
        host, port = parsed.netloc.split(":")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        
        if result == 0:
            print(f"✅ Tor прокси доступен на {host}:{port}")
            return True
        else:
            print(f"❌ Tor прокси недоступен на {host}:{port}")
            print("   Убедитесь, что Tor запущен!")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки прокси: {e}")
        return False


def check_tor_connection():
    """Проверить работоспособность Tor через реальный запрос"""
    print("\n🌐 Проверка соединения через Tor...")
    print("   (Это может занять 30-120 секунд при первом подключении)")
    
    proxy = {
        'http': Config.TOR_PROXY,
        'https': Config.TOR_PROXY
    }
    
    try:
        start_time = time.time()
        response = requests.get(
            "https://check.torproject.org",
            proxies=proxy,
            timeout=Config.TOR_CONNECTION_TIMEOUT
        )
        elapsed = time.time() - start_time
        
        if "Congratulations" in response.text:
            print(f"✅ Tor работает! Время подключения: {elapsed:.1f}с")
            return True
        else:
            print("⚠️  Tor прокси работает, но соединение не установлено")
            return False
    except requests.exceptions.Timeout:
        print("⏳ Таймаут при подключении")
        print("   Это нормально для первого подключения - Tor устанавливает цепочку узлов")
        print("   Попробуйте подождать 1-2 минуты и запустить проверку снова")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def main():
    """Главная функция"""
    print("=" * 60)
    print("🕵️  Проверка Tor для Robin")
    print("=" * 60)
    print()
    
    # Проверка прокси
    proxy_ok = check_tor_proxy()
    if not proxy_ok:
        print("\n💡 Решение:")
        print("   1. Убедитесь, что Tor Browser запущен")
        print("   2. Или запустите Tor daemon: sudo systemctl start tor")
        sys.exit(1)
    
    # Проверка соединения
    connection_ok = check_tor_connection()
    
    print()
    print("=" * 60)
    if connection_ok:
        print("✅ Tor готов к работе!")
        print("   Можете запускать Robin: python main.py cli --query 'test'")
    else:
        print("⚠️  Tor прокси работает, но соединение медленное")
        print("   Это нормально - подождите 1-2 минуты и попробуйте снова")
    print("=" * 60)


if __name__ == "__main__":
    main()

