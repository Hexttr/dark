# ✅ Robin готов к использованию!

## 🎉 Настройка завершена

Все компоненты настроены и готовы к работе:
- ✅ Python 3.14.1
- ✅ Все зависимости установлены
- ✅ Tor настроен (порт 9150)
- ✅ Ollama работает (модель llama3.1:8b)
- ✅ Конфигурация создана (.env)

## 🚀 Быстрый старт

### CLI режим (командная строка)

```bash
# Простой тест
python main.py cli --query "test search"

# С выбором модели
python main.py cli --model llama3.1 --query "password leak database"

# С сохранением результата
python main.py cli --query "ransomware payments" --output report.txt
```

### Web UI режим (веб-интерфейс)

```bash
python main.py ui
```

Затем откройте в браузере: **http://localhost:8501**

## 📝 Примеры использования

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

## 🔧 Полезные команды

### Проверка настройки
```bash
python test_setup.py
```

### Проверка Tor
```bash
python check_tor.py
```

### Справка
```bash
python main.py --help
python main.py cli --help
```

## ⚙️ Текущие настройки

- **Tor:** socks5://127.0.0.1:9150
- **Ollama:** http://127.0.0.1:11434
- **Модель:** llama3.1:8b
- **Потоков:** 10 (по умолчанию)

Настройки можно изменить в файле `.env`

## 📚 Документация

- `README.md` - Основная документация
- `GUIDE_RU.md` - Полное руководство на русском
- `EXAMPLES.md` - Готовые примеры команд
- `TOR_INFO.md` - Информация о работе с Tor

## ⚠️ Важно

- Первый запрос через Tor может занять 30-120 секунд (это нормально!)
- Убедитесь, что Tor Browser запущен перед использованием
- Используйте только для законных целей

## 🎯 Готовы начать?

Запустите простой тест:
```bash
python main.py cli --query "test search"
```

Или откройте веб-интерфейс:
```bash
python main.py ui
```

**Удачи в расследованиях! 🕵️**


