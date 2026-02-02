@echo off
chcp 65001 >nul
echo ============================================================
echo Автоматический push изменений в GitHub
echo ============================================================
echo.

git add .
echo Добавлены изменения в staging...

git status --short
echo.

set /p commit_msg="Введите сообщение коммита (или Enter для автоматического): "
if "%commit_msg%"=="" (
    set commit_msg=Update: автоматический коммит %date% %time%
)

git commit -m "%commit_msg%"
echo.

echo Отправка изменений в GitHub...
git push origin main

echo.
echo ============================================================
echo Готово! Изменения отправлены в репозиторий.
echo ============================================================
pause

