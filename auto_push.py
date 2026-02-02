"""
Автоматический push изменений в GitHub после правок
Используется внутренне для автоматизации
"""
import subprocess
import sys
from datetime import datetime

def auto_push(description="Update: автоматический коммит"):
    """Автоматически добавить, закоммитить и запушить изменения"""
    try:
        # Добавляем все изменения
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Создаем коммит
        commit_msg = f"{description} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        
        # Пушим в GitHub
        result = subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True, text=True)
        print(f"✅ Изменения отправлены в GitHub: {commit_msg}")
        return True
    except subprocess.CalledProcessError as e:
        # Если нет изменений, это нормально
        if "nothing to commit" in str(e.stderr) or "no changes" in str(e.stderr).lower():
            print("ℹ️ Нет изменений для коммита")
            return True
        print(f"⚠️ Ошибка при пуше: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")
        return False

if __name__ == "__main__":
    description = sys.argv[1] if len(sys.argv) > 1 else "Update"
    auto_push(description)

