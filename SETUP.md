# 🚀 Быстрая установка и запуск

## Шаг 1: Установка зависимостей системы

### Tor
```bash
# Windows (WSL)
sudo apt install tor
sudo systemctl start tor

# Linux
sudo apt install tor
sudo systemctl start tor

# Mac
brew install tor
brew services start tor
```

### Ollama
1. Скачайте с https://ollama.ai/
2. Установите и запустите
3. Скачайте модель:
```bash
ollama pull llama3.1
# или
ollama pull mistral
```

## Шаг 2: Установка Python зависимостей

```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Шаг 3: Настройка конфигурации

```bash
# Скопировать пример конфигурации
cp env.example .env

# Отредактировать при необходимости (обычно не требуется)
```

## Шаг 4: Проверка

```bash
# Проверить Tor
curl --socks5 127.0.0.1:9050 https://check.torproject.org

# Проверить Ollama
curl http://127.0.0.1:11434/api/tags
```

## Шаг 5: Запуск

### CLI режим
```bash
python main.py cli --query "test search"
```

### Web UI режим
```bash
python main.py ui
# Откройте http://localhost:8501
```

## 🔧 Решение проблем

### Tor не работает
```bash
# Проверить статус
sudo systemctl status tor

# Перезапустить
sudo systemctl restart tor
```

### Ollama не отвечает
```bash
# Проверить, что Ollama запущен
ollama serve

# Проверить модели
ollama list
```

### Ошибки импорта
```bash
# Убедитесь, что виртуальное окружение активировано
# Переустановите зависимости
pip install -r requirements.txt --force-reinstall
```


