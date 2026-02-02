# ⚡ Быстрый старт Robin - пошаговая инструкция

## 🎯 Цель: Запустить Robin за 10 минут

---

## Шаг 1: Установка Tor (5 минут)

### Windows

**Вариант A: Через установщик**
1. Скачайте Tor Browser с https://www.torproject.org/download/
2. Установите Tor Browser
3. Запустите Tor Browser хотя бы один раз
4. Tor будет работать в фоне

**Вариант B: Через Chocolatey (если установлен)**
```powershell
choco install tor
```

**Вариант C: Через WSL (рекомендуется для разработки)**
```bash
sudo apt update
sudo apt install tor
sudo systemctl start tor
sudo systemctl enable tor
```

### Linux/WSL
```bash
sudo apt update
sudo apt install tor
sudo systemctl start tor
sudo systemctl enable tor

# Проверить, что Tor работает
sudo systemctl status tor
```

### Mac
```bash
brew install tor
brew services start tor

# Проверить статус
brew services list | grep tor
```

**Проверка работы Tor:**
```bash
# Проверить, что Tor слушает на порту 9050
netstat -an | grep 9050
# или
ss -tuln | grep 9050
```

---

## Шаг 2: Получение API ключа (2 минуты)

Выберите один из вариантов:

### Вариант A: OpenAI (GPT-4.1)
1. Зайдите на https://platform.openai.com/api-keys
2. Создайте новый API ключ
3. Скопируйте ключ (он показывается только один раз!)

### Вариант B: Anthropic (Claude)
1. Зайдите на https://console.anthropic.com/
2. Создайте аккаунт или войдите
3. Перейдите в Settings → API Keys
4. Создайте новый ключ

### Вариант C: Google (Gemini)
1. Зайдите на https://aistudio.google.com/app/apikey
2. Создайте новый API ключ

### Вариант D: Ollama (локально, бесплатно)
1. Установите Ollama: https://ollama.ai/
2. Запустите Ollama:
```bash
ollama serve
```
3. В другом терминале скачайте модель:
```bash
ollama pull llama3.1
```

---

## Шаг 3: Установка Robin (3 минуты)

### Вариант A: Docker (самый простой) ⭐ РЕКОМЕНДУЕТСЯ

```bash
# 1. Скачать образ
docker pull apurvsg/robin:latest

# 2. Создать .env файл
cat > .env << EOF
OPENAI_API_KEY=your-key-here
# или
ANTHROPIC_API_KEY=your-key-here
# или
GOOGLE_API_KEY=your-key-here
# или для Ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
EOF

# 3. Запустить веб-интерфейс
docker run --rm \
   -v "$(pwd)/.env:/app/.env" \
   --add-host=host.docker.internal:host-gateway \
   -p 8501:8501 \
   apurvsg/robin:latest ui --ui-port 8501 --ui-host 0.0.0.0
```

**Откройте в браузере:** http://localhost:8501

### Вариант B: Python (для разработки)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/apurvsinghgautam/robin.git
cd robin

# 2. Создать виртуальное окружение
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env файл
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env

# 5. Отредактировать .env и добавить ваш API ключ
notepad .env  # Windows
nano .env     # Linux/Mac
```

---

## Шаг 4: Первый запуск (1 минута)

### CLI режим (командная строка)

```bash
# Простой тест
python main.py cli --model gpt-4.1 --query "test search" --threads 5

# Или если используете Docker
docker run --rm \
   -v "$(pwd)/.env:/app/.env" \
   --add-host=host.docker.internal:host-gateway \
   apurvsg/robin:latest cli --model gpt-4.1 --query "test search" --threads 5
```

### Web UI режим (веб-интерфейс)

```bash
# Python
python main.py ui

# Docker (уже запущен выше)
# Просто откройте http://localhost:8501
```

---

## 🎉 Готово! Теперь попробуйте реальный запрос

### Пример 1: Проверка утечек паролей
```bash
python main.py cli --model gpt-4.1 --query "password leak database 2024" --threads 10 --output first_search.txt
```

### Пример 2: Поиск информации о ransomware
```bash
python main.py cli --model claude-3-5-sonnet-latest --query "ransomware payments victims 2024" --threads 8
```

### Пример 3: Быстрый поиск с Gemini
```bash
python main.py cli --model gemini-2.5-flash --query "phishing campaigns 2024" --threads 6
```

---

## 🔧 Решение проблем

### Проблема: "Tor не запущен"
**Решение:**
```bash
# Linux/WSL
sudo systemctl start tor
sudo systemctl status tor

# Mac
brew services start tor

# Windows - запустите Tor Browser
```

### Проблема: "API ключ не работает"
**Решение:**
1. Проверьте, что ключ правильно скопирован в `.env`
2. Убедитесь, что нет лишних пробелов
3. Проверьте баланс API (для платных сервисов)
4. Для Ollama убедитесь, что сервер запущен

### Проблема: "Connection refused"
**Решение:**
- Проверьте, что Tor работает: `netstat -an | grep 9050`
- Проверьте файрвол
- Попробуйте перезапустить Tor

### Проблема: "Module not found"
**Решение:**
```bash
# Убедитесь, что виртуальное окружение активировано
pip install -r requirements.txt
```

---

## 📋 Чек-лист перед использованием

- [ ] Tor установлен и запущен
- [ ] API ключ получен и добавлен в `.env`
- [ ] Robin установлен (Docker или Python)
- [ ] Тестовый запрос выполнен успешно
- [ ] Понимаете, как использовать команды

---

## 🚀 Следующие шаги

1. **Изучите примеры:** Откройте `EXAMPLES.md` для готовых команд
2. **Прочитайте руководство:** Смотрите `GUIDE_RU.md` для детальной информации
3. **Экспериментируйте:** Попробуйте разные запросы и модели
4. **Сохраняйте результаты:** Всегда используйте `--output` для важных расследований

---

## 💡 Полезные команды

### Проверка статуса Tor
```bash
# Linux
sudo systemctl status tor

# Mac
brew services list | grep tor

# Проверка порта
netstat -an | grep 9050
```

### Просмотр логов Robin
```bash
# Если что-то не работает, проверьте вывод команды
python main.py cli --model gpt-4.1 --query "test" --threads 5 -v
```

### Обновление Robin (Docker)
```bash
docker pull apurvsg/robin:latest
```

### Обновление Robin (Python)
```bash
cd robin
git pull
pip install -r requirements.txt --upgrade
```

---

## 🎓 Готовы начать?

Откройте `EXAMPLES.md` и скопируйте любую команду, заменив параметры на свои!

**Удачи в расследованиях! 🕵️‍♂️**


