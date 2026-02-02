"""
Автоматический скрипт для пуша изменений в GitHub
"""
import subprocess
import sys
from datetime import datetime

def run_command(cmd, description):
    """Выполнить команду git"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            if result.stdout.strip():
                print(result.stdout)
            return True
        else:
            print(f"❌ Ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return False

def main():
    """Главная функция"""
    print("=" * 60)
    print("🚀 Автоматический push изменений в GitHub")
    print("=" * 60)
    print()
    
    # Проверка статуса
    print("📊 Проверка статуса репозитория...")
    run_command("git status --short", "Проверка изменений")
    print()
    
    # Добавление изменений
    if not run_command("git add .", "Добавление изменений"):
        print("⚠️ Нет изменений для коммита")
        return
    
    # Сообщение коммита
    commit_msg = input("Введите сообщение коммита (или Enter для автоматического): ").strip()
    if not commit_msg:
        commit_msg = f"Update: автоматический коммит {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Коммит
    if not run_command(f'git commit -m "{commit_msg}"', "Создание коммита"):
        print("⚠️ Нет изменений для коммита")
        return
    
    # Push
    if run_command("git push origin main", "Отправка в GitHub"):
        print()
        print("=" * 60)
        print("✅ Готово! Изменения отправлены в репозиторий.")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("❌ Ошибка при отправке изменений")
        print("=" * 60)

if __name__ == "__main__":
    main()

