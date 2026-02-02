# 🚀 Готовые команды Robin - копируй и используй

## 📧 Проверка утечек данных

### Проверка email в утечках
```bash
robin cli --model gpt-4.1 --query "email password leak your-email@example.com database" --threads 10 --output email_check.txt
```

### Проверка паролей для конкретного сервиса
```bash
robin cli --model claude-3-5-sonnet-latest --query "stolen credentials gmail yahoo outlook accounts database" --threads 12
```

### Поиск новых утечек баз данных
```bash
robin cli --model gemini-2.5-flash --query "new database leak 2024 user credentials passwords" --threads 10 --output new_leaks.txt
```

---

## 🏢 Безопасность компании

### Мониторинг упоминаний компании
```bash
robin cli --model gpt-4.1 --query "company-name data breach ransomware attack customer data" --threads 12 --output company_monitoring.txt
```

### Поиск продажи данных компании
```bash
robin cli --model claude-3-5-sonnet-latest --query "stolen database company-name customer information for sale" --threads 10
```

### Проверка планируемых атак
```bash
robin cli --model gpt-4.1 --query "target company-name DDoS attack planned infrastructure" --threads 8
```

---

## 🎣 Фишинг и мошенничество

### Поиск фишинговых кампаний
```bash
robin cli --model gemini-2.5-flash --query "phishing campaigns 2024 fake login pages banking email" --threads 8
```

### Исследование фишинговых сайтов
```bash
robin cli --model gpt-4.1 --query "fake bank website phishing kit tutorial domain" --threads 6 --output phishing_sites.txt
```

### Мониторинг новых схем мошенничества
```bash
robin cli --model claude-3-5-sonnet-latest --query "scam scheme cryptocurrency investment fraud 2024" --threads 10
```

---

## 🔑 API ключи и токены

### Поиск утечек API ключей
```bash
robin cli --model gpt-4.1 --query "exposed API keys tokens github credentials leaked" --threads 10 --output api_keys.txt
```

### Поиск утечек AWS ключей
```bash
robin cli --model claude-3-5-sonnet-latest --query "AWS access keys leaked S3 bucket credentials exposed" --threads 12
```

### Поиск утечек токенов доступа
```bash
robin cli --model gemini-2.5-flash --query "OAuth tokens access tokens leaked GitHub GitLab" --threads 8
```

---

## 💰 Ransomware и кибератаки

### Исследование ransomware-платежей
```bash
robin cli --model gpt-4.1 --query "ransomware payments victim list 2024 LockBit BlackCat" --threads 12 --output ransomware_victims.txt
```

### Поиск новых ransomware-групп
```bash
robin cli --model llama3.1 --query "new ransomware group leak site victims data" --threads 10
```

### Мониторинг активности хакерских групп
```bash
robin cli --model claude-3-5-sonnet-latest --query "hacker group Conti LockBit REvil activities 2024" --threads 12
```

---

## 👥 Хакерские форумы и сообщества

### Поиск хакерских форумов
```bash
robin cli --model gpt-4.1 --query "hacker forum marketplace stolen accounts credentials" --threads 10
```

### Исследование торговых площадок
```bash
robin cli --model claude-3-5-sonnet-latest --query "dark web marketplace stolen data credit cards for sale" --threads 12
```

### Поиск чатов и каналов хакеров
```bash
robin cli --model gemini-2.5-flash --query "hacker chat telegram channel cybercrime discussion" --threads 8
```

---

## 🐛 Уязвимости и эксплойты

### Поиск zero-day уязвимостей
```bash
robin cli --model gpt-4.1 --query "zero-day vulnerability exploit CVE-2024 unpatched" --threads 10 --output zero_days.txt
```

### Исследование новых эксплойтов
```bash
robin cli --model llama3.1 --query "new exploit RCE SQL injection remote code execution" --threads 8
```

### Мониторинг продажи эксплойтов
```bash
robin cli --model claude-3-5-sonnet-latest --query "exploit for sale zero-day vulnerability price" --threads 10
```

---

## 📱 Утечки мобильных приложений

### Поиск утечек данных приложений
```bash
robin cli --model gpt-4.1 --query "mobile app database leak user data Android iOS" --threads 10
```

### Исследование утечек социальных сетей
```bash
robin cli --model gemini-2.5-flash --query "social media platform database dump leaked passwords 2024" --threads 12
```

---

## 🔍 Исследовательские запросы

### Общий поиск угроз
```bash
robin cli --model gpt-4.1 --query "cyber threat intelligence 2024 malware attacks" --threads 12 --output threat_intel.txt
```

### Поиск информации о конкретном инциденте
```bash
robin cli --model claude-3-5-sonnet-latest --query "data breach incident company-name date 2024 details" --threads 10
```

### Исследование трендов в киберпреступности
```bash
robin cli --model gemini-2.5-flash --query "cybercrime trends 2024 new attack methods techniques" --threads 8
```

---

## 💻 Короткие команды (сокращенный синтаксис)

### Быстрая проверка
```bash
robin cli -m gpt-4.1 -q "password leak database" -t 10
```

### С сохранением результата
```bash
robin cli -m claude-3-5-sonnet-latest -q "ransomware victims" -t 12 -o report.txt
```

### С локальной моделью Ollama
```bash
robin cli -m llama3.1 -q "zero-day exploit" -t 8
```

### Быстрый поиск с Gemini
```bash
robin cli -m gemini-2.5-flash -q "phishing campaign" -t 6
```

---

## 🎯 Специализированные запросы

### Поиск конкретного домена в утечках
```bash
robin cli --model gpt-4.1 --query "domain example.com credentials leak database" --threads 10
```

### Поиск информации о конкретном человеке (для защиты)
```bash
robin cli --model claude-3-5-sonnet-latest --query "personal information doxxing leak full name address" --threads 8
```

### Мониторинг бренда
```bash
robin cli --model gpt-4.1 --query "brand-name fake products counterfeit marketplace" --threads 10 --output brand_monitoring.txt
```

---

## 📊 Параметры для разных задач

### Для быстрых проверок (меньше потоков)
```bash
robin cli -m gemini-2.5-flash -q "your query" -t 5
```

### Для глубоких расследований (больше потоков)
```bash
robin cli -m gpt-4.1 -q "your query" -t 15 -o detailed_report.txt
```

### Для приватных расследований (локальная модель)
```bash
robin cli -m llama3.1 -q "your query" -t 8
```

---

## ⚡ Полезные комбинации

### Ежедневный мониторинг компании
```bash
robin cli -m gpt-4.1 -q "company-name security breach leak" -t 12 -o daily_check_$(date +%Y%m%d).txt
```

### Еженедельный отчет об угрозах
```bash
robin cli -m claude-3-5-sonnet-latest -q "cyber threats week ransomware phishing" -t 10 -o weekly_threats_$(date +%Y%m%d).txt
```

### Проверка после инцидента
```bash
robin cli -m gpt-4.1 -q "incident company-name data breach details" -t 15 -o incident_analysis.txt
```

---

## 🔄 Замена переменных в командах

Замените в примерах:
- `your-email@example.com` → ваш реальный email
- `company-name` → название вашей компании
- `domain example.com` → ваш домен
- `your query` → ваш поисковый запрос

---

## 💡 Советы по использованию

1. **Начните с простых запросов** - проверьте базовую функциональность
2. **Используйте английский язык** - запросы работают лучше на английском
3. **Сохраняйте результаты** - всегда используйте `--output` для важных расследований
4. **Экспериментируйте с моделями** - разные модели дают разные результаты
5. **Начинайте с малого количества потоков** - увеличивайте постепенно

---

**Примечание:** Все команды предполагают, что:
- Tor установлен и запущен
- API ключи настроены в `.env` файле
- Robin установлен и готов к использованию


