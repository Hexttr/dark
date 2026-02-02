"""
Простой скрипт для запуска веб-интерфейса
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

import subprocess

if __name__ == "__main__":
    print("=" * 60)
    print("Запуск веб-интерфейса Robin...")
    print("=" * 60)
    print()
    print("Веб-интерфейс будет доступен по адресу:")
    print("  http://localhost:8501")
    print()
    print("Нажмите Ctrl+C для остановки")
    print("=" * 60)
    print()
    
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'ui.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--server.headless', 'true'
        ])
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    except Exception as e:
        print(f"Ошибка: {e}")
        print("\nПопробуйте запустить вручную:")
        print("  streamlit run ui.py")


