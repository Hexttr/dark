"""
Финальная настройка и проверка
"""
import sys
import os
import socket

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def find_tor_port():
    """Поиск порта Tor"""
    common_ports = [9050, 9150, 9051, 9151]
    print("Поиск Tor на стандартных портах...")
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                print(f"  OK - Tor найден на порту {port}")
                return port
        except:
            pass
    
    print("  WARNING - Tor не найден на стандартных портах")
    return None


def update_env_file(port):
    """Обновить .env файл с правильным портом"""
    if port and port != 9050:
        print(f"\nОбновление .env файла с портом {port}...")
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Заменить порт в TOR_PROXY
            new_content = content.replace(
                'TOR_PROXY=socks5://127.0.0.1:9050',
                f'TOR_PROXY=socks5://127.0.0.1:{port}'
            )
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  OK - .env обновлен")
            return True
        except Exception as e:
            print(f"  ERROR - {e}")
            return False
    return True


def main():
    print("=" * 60)
    print("Финальная настройка Robin")
    print("=" * 60)
    print()
    
    # Поиск Tor
    tor_port = find_tor_port()
    
    if tor_port:
        update_env_file(tor_port)
        print()
        print("=" * 60)
        print("OK - Настройка завершена!")
        print("=" * 60)
        print()
        print("Теперь можно запускать:")
        print("  python main.py cli --query 'test search'")
        print("  или")
        print("  python main.py ui")
    else:
        print()
        print("=" * 60)
        print("WARNING - Tor не найден")
        print("=" * 60)
        print()
        print("Убедитесь, что:")
        print("  1. Tor Browser запущен")
        print("  2. Или Tor daemon запущен: sudo systemctl start tor")
        print()
        print("После запуска Tor запустите снова:")
        print("  python test_setup.py")


if __name__ == "__main__":
    main()


