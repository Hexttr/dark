# 🕵️ Robin - AI-Powered Dark Web OSINT Tool

AI-инструмент для OSINT-расследований в dark web с использованием локального LLM (Ollama).

## ✨ Особенности

- 🤖 **Локальный AI** - использует Ollama для приватной обработки данных
- 🔒 **Приватность** - все данные обрабатываются локально, без облачных API
- 🌐 **Tor интеграция** - безопасный доступ к dark web
- 🚀 **Многопоточность** - быстрый скрапинг результатов
- 💻 **CLI и Web UI** - два режима работы
- 📊 **Автоматические отчеты** - AI генерирует итоговые отчеты

## 🏗️ Архитектура

```
User Query
    ↓
[LLM] - Генерация поисковых запросов (Ollama)
    ↓
[Search] - Поиск через Tor в dark web
    ↓
[Scrape] - Многопоточный скрапинг результатов
    ↓
[LLM] - Фильтрация и анализ (Ollama)
    ↓
[LLM] - Генерация итогового отчета (Ollama)
    ↓
Report
```

## 📋 Требования

- Python 3.10+
- Tor (установлен и запущен)
- Ollama (установлен и запущен с моделью)

## 🚀 Установка

### 1. Установите Tor

**Windows:**
- Скачайте Tor Browser с https://www.torproject.org/
- Или используйте WSL: `sudo apt install tor`

**Linux:**
```bash
sudo apt install tor
sudo systemctl start tor
```

**Mac:**
```bash
brew install tor
brew services start tor
```

### 2. Установите Ollama

Скачайте с https://ollama.ai/ и установите.

Запустите Ollama и скачайте модель:
```bash
ollama serve
# В другом терминале:
ollama pull llama3.1
```

### 3. Установите зависимости

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте (Windows)
venv\Scripts\activate

# Активируйте (Linux/Mac)
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt
```

### 4. Настройте конфигурацию

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env при необходимости
# По умолчанию используются стандартные настройки
```

## 💻 Использование

### CLI режим

```bash
# Базовое использование
python main.py cli --query "password leak database 2024"

# С выбором модели
python main.py cli --model llama3.1 --query "ransomware payments" --threads 12

# С сохранением в файл
python main.py cli -m mistral -q "data breach" -o report.txt
```

### Web UI режим

```bash
python main.py ui
```

Откройте браузер: http://localhost:8501

## 📖 Примеры

### Проверка утечек данных
```bash
python main.py cli --query "email password leak database 2024" --threads 10
```

### Исследование ransomware
```bash
python main.py cli --model llama3.1 --query "ransomware payments victims" --threads 8
```

### Мониторинг компании
```bash
python main.py cli --query "company-name data breach" --output company_report.txt
```

## ⚙️ Конфигурация

Настройки в файле `.env`:

- `OLLAMA_BASE_URL` - URL Ollama сервера (по умолчанию: http://127.0.0.1:11434)
- `OLLAMA_MODEL` - Модель по умолчанию (по умолчанию: llama3.1)
- `TOR_PROXY` - Tor прокси (по умолчанию: socks5://127.0.0.1:9050)
- `MAX_THREADS` - Количество потоков для скрапинга (по умолчанию: 10)

## 🧩 Компоненты

- **config.py** - Конфигурация и настройки
- **llm.py** - Работа с Ollama LLM
- **llm_utils.py** - Утилиты для промптов
- **search.py** - Поиск в dark web через Tor
- **scrape.py** - Многопоточный скрапинг
- **main.py** - CLI интерфейс
- **ui.py** - Веб-интерфейс Streamlit

## ⚠️ Важные предупреждения

- Используйте только для **законных целей**
- Убедитесь, что Tor запущен перед использованием
- Убедитесь, что Ollama запущен и модель загружена
- Соблюдайте законы вашей юрисдикции

## 📝 Лицензия

MIT License

## 🙏 Благодарности

Вдохновлено проектом [Robin](https://github.com/apurvsinghgautam/robin) от apurvsinghgautam.


