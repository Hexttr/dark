# 🎯 Практическое руководство по использованию Robin

## 📋 Что такое Robin простыми словами?

**Robin** - это умный помощник, который:
1. Принимает ваш вопрос (например, "найти утечки моих паролей")
2. Ищет информацию в dark web через специальные поисковые системы
3. Фильтрует результаты с помощью AI
4. Выдает вам готовый отчет

---

## 🚀 Быстрые примеры использования

### Пример 1: Проверка утечки ваших данных

**Ситуация:** Вы хотите проверить, не были ли ваши email/пароли скомпрометированы и не продаются ли они в dark web.

```bash
# Проверка утечек email
robin cli --model gpt-4.1 --query "email password leak your-email@example.com" --threads 8

# Проверка утечек паролей для конкретного сервиса
robin cli --model gpt-4.1 --query "stolen credentials gmail accounts database" --threads 10
```

**Что произойдет:**
- Robin сформулирует умные запросы для поиска
- Найдет упоминания вашего email в базах данных утечек
- Отфильтрует релевантные результаты
- Создаст отчет с найденной информацией

---

### Пример 2: Мониторинг кибератак на вашу компанию

**Ситуация:** Вы хотите узнать, не упоминается ли ваша компания в контексте кибератак или утечек данных.

```bash
# Поиск упоминаний компании
robin cli --model claude-3-5-sonnet-latest --query "data breach company-name ransomware attack" --threads 12 --output company_security_report.txt

# Поиск продажи данных компании
robin cli --model gpt-4.1 --query "stolen database company-name customer data for sale" --threads 8
```

**Результат:** Отчет покажет:
- Упоминания вашей компании в dark web
- Продаются ли данные ваших клиентов
- Планируются ли атаки на вашу инфраструктуру

---

### Пример 3: Исследование фишинговых кампаний

**Ситуация:** Вы хотите узнать о новых фишинговых схемах, чтобы защитить своих сотрудников.

```bash
robin cli --model gemini-2.5-flash --query "phishing campaigns 2024 fake login pages banking" --threads 5

# Поиск конкретных фишинговых сайтов
robin cli --model gpt-4.1 --query "fake bank website phishing kit tutorial" --threads 6
```

---

### Пример 4: Мониторинг утечек API ключей и токенов

**Ситуация:** Вы разработчик и хотите проверить, не попали ли ваши API ключи в публичный доступ.

```bash
# Поиск утечек API ключей
robin cli --model gpt-4.1 --query "exposed API keys tokens github credentials" --threads 8 --output api_keys_report.txt

# Поиск конкретного сервиса
robin cli --model claude-3-5-sonnet-latest --query "AWS access keys leaked S3 bucket credentials" --threads 10
```

---

### Пример 5: Исследование ransomware-групп

**Ситуация:** Вы хотите понять, какие ransomware-группы активны и на кого они нацелены.

```bash
# Поиск информации о ransomware-платежах
robin cli --model gpt-4.1 --query "ransomware payments victim list 2024" --threads 12

# Поиск новых ransomware-групп
robin cli --model llama3.1 --query "new ransomware group leak site victims" --threads 8
```

---

### Пример 6: Поиск информации о киберпреступниках

**Ситуация:** Вы проводите расследование и ищете информацию о конкретных хакерах или группах.

```bash
# Поиск информации о хакерских группах
robin cli --model gpt-4.1 --query "hacker group Conti LockBit activities" --threads 10

# Поиск форумов и чатов хакеров
robin cli --model claude-3-5-sonnet-latest --query "hacker forum marketplace stolen accounts" --threads 8
```

---

### Пример 7: Мониторинг утечек баз данных

**Ситуация:** Вы хотите узнать, не были ли взломаны популярные сервисы, которыми вы пользуетесь.

```bash
# Поиск новых утечек баз данных
robin cli --model gemini-2.5-flash --query "new database leak 2024 user credentials" --threads 10 --output database_leaks.txt

# Поиск конкретного сервиса
robin cli --model gpt-4.1 --query "social media platform database dump leaked passwords" --threads 8
```

---

## 🛠️ Пошаговая инструкция для начинающих

### Шаг 1: Установка Tor

**Windows:**
```powershell
# Через Chocolatey
choco install tor

# Или скачайте с https://www.torproject.org/
```

**Linux/WSL:**
```bash
sudo apt install tor
sudo systemctl start tor
```

**Mac:**
```bash
brew install tor
brew services start tor
```

### Шаг 2: Установка Robin

**Вариант A: Docker (рекомендуется)**
```bash
# Скачать образ
docker pull apurvsg/robin:latest

# Запустить веб-интерфейс
docker run --rm \
   -v "$(pwd)/.env:/app/.env" \
   --add-host=host.docker.internal:host-gateway \
   -p 8501:8501 \
   apurvsg/robin:latest ui --ui-port 8501 --ui-host 0.0.0.0
```

**Вариант B: Python (для разработки)**
```bash
# Клонировать репозиторий
git clone https://github.com/apurvsinghgautam/robin.git
cd robin

# Установить зависимости
pip install -r requirements.txt
```

### Шаг 3: Настройка API ключей

Создайте файл `.env`:
```env
# OpenAI
OPENAI_API_KEY=your-openai-key-here

# Или Anthropic
ANTHROPIC_API_KEY=your-anthropic-key-here

# Или Google
GOOGLE_API_KEY=your-google-key-here

# Или для локального Ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

### Шаг 4: Первый запуск

**CLI режим:**
```bash
# Простой запрос
python main.py cli --model gpt-4.1 --query "test search" --threads 5

# Или если используете бинарник
robin cli --model gpt-4.1 --query "test search" --threads 5
```

**Web UI режим:**
```bash
# Запустить веб-интерфейс
python main.py ui

# Открыть в браузере: http://localhost:8501
```

---

## 📊 Понимание параметров

### `--model` или `-m`
Выбор AI модели:
- `gpt-4.1` - OpenAI GPT-4 (самый умный, но платный)
- `claude-3-5-sonnet-latest` - Anthropic Claude (хороший баланс)
- `gemini-2.5-flash` - Google Gemini (быстрый и дешевый)
- `llama3.1` - Ollama локальная модель (бесплатно, но нужен Ollama)

### `--query` или `-q`
Ваш поисковый запрос. Может быть:
- Простым: `"password leak"`
- Сложным: `"stolen credentials gmail accounts database 2024"`
- Специфичным: `"company-name data breach customer information"`

### `--threads` или `-t`
Количество параллельных потоков для поиска (5-15 обычно достаточно):
- Меньше потоков = медленнее, но стабильнее
- Больше потоков = быстрее, но может быть нестабильно

### `--output` или `-o`
Имя файла для сохранения отчета:
```bash
robin cli --model gpt-4.1 --query "test" --output my_report.txt
```

---

## 💡 Практические советы

### 1. Формулировка запросов
✅ **Хорошо:**
- "email password leak database 2024"
- "stolen credentials banking accounts"
- "data breach company-name customer data"

❌ **Плохо:**
- "hack" (слишком общий)
- "password" (слишком простой)
- "найти пароли" (используйте английский)

### 2. Выбор модели
- **Для важных расследований:** GPT-4.1 или Claude
- **Для быстрых проверок:** Gemini Flash
- **Для приватности:** Ollama (локально)

### 3. Сохранение результатов
Всегда используйте `--output` для важных расследований:
```bash
robin cli --model gpt-4.1 --query "your query" --output investigation_2024_01_15.txt
```

### 4. Оптимизация потоков
- Начинайте с 5-8 потоков
- Увеличивайте до 12-15 для больших запросов
- Следите за стабильностью Tor соединения

---

## ⚠️ Важные предупреждения

1. **Законность:** Используйте только для законных целей (защита своих данных, расследования с разрешения)
2. **Приватность:** Не отправляйте чувствительные данные в AI модели без необходимости
3. **Tor:** Убедитесь, что Tor работает перед запуском
4. **API ключи:** Храните `.env` файл в безопасности, не коммитьте в Git

---

## 🔍 Типичные сценарии использования

### Сценарий 1: "Проверить, не украли ли мои данные"
```bash
robin cli --model gpt-4.1 \
  --query "email password leak your-email@example.com database dump" \
  --threads 10 \
  --output my_data_check.txt
```

### Сценарий 2: "Мониторинг безопасности компании"
```bash
robin cli --model claude-3-5-sonnet-latest \
  --query "company-name data breach ransomware attack leak" \
  --threads 12 \
  --output company_monitoring_$(date +%Y%m%d).txt
```

### Сценарий 3: "Исследование новой угрозы"
```bash
robin cli --model gemini-2.5-flash \
  --query "new malware ransomware 2024 zero-day exploit" \
  --threads 8 \
  --output threat_research.txt
```

---

## 📝 Примеры реальных команд

```bash
# 1. Проверка утечек паролей
robin cli -m gpt-4.1 -q "password leak database 2024" -t 10 -o passwords_leak.txt

# 2. Поиск информации о хакерских группах
robin cli -m claude-3-5-sonnet-latest -q "LockBit ransomware group activities victims" -t 12

# 3. Мониторинг фишинга
robin cli -m gemini-2.5-flash -q "phishing campaign fake banking website 2024" -t 8

# 4. Поиск утечек API ключей
robin cli -m gpt-4.1 -q "exposed API keys AWS GitHub credentials" -t 10 -o api_keys.txt

# 5. Исследование новых угроз
robin cli -m llama3.1 -q "zero-day vulnerability exploit CVE-2024" -t 6
```

---

## 🎓 Что дальше?

1. Начните с простых запросов
2. Экспериментируйте с разными моделями
3. Сохраняйте важные результаты
4. Изучайте отчеты для понимания угроз
5. Используйте для проактивной защиты

**Помните:** Robin - это инструмент для защиты, а не для атак. Используйте ответственно! 🛡️


