# 🔄 Рабочий процесс с Git

## 📋 Быстрый старт

### Первый раз (уже сделано):
```bash
git init
git remote add origin https://github.com/Hexttr/dark.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

## 🚀 Автоматический push после правок

### Вариант 1: Использовать скрипт (рекомендуется)

**Windows:**
```bash
push_changes.bat
```

**Или Python:**
```bash
python push_changes.py
```

### Вариант 2: Ручной push

```bash
git add .
git commit -m "Описание изменений"
git push origin main
```

## 📝 Примеры сообщений коммитов:

```
fix: исправлена проблема с таймаутами
feat: добавлена поддержка DuckDuckGo
refactor: оптимизирован парсинг результатов
docs: обновлена документация
perf: улучшена производительность поиска
```

## 🔄 После каждой правки:

1. **Сохраните файлы**
2. **Запустите:** `python push_changes.py` или `push_changes.bat`
3. **Введите описание** изменений (или нажмите Enter для автоматического)
4. **Готово!** Изменения отправлены в GitHub

## 📊 Проверка статуса:

```bash
git status          # Показать изменения
git log --oneline   # Показать историю коммитов
git diff            # Показать различия
```

## 🔗 Репозиторий:

**GitHub:** https://github.com/Hexttr/dark

---

**Теперь все изменения автоматически синхронизируются с GitHub!** ✅

