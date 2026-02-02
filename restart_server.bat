@echo off
chcp 65001 >nul
echo ============================================================
echo Перезапуск веб-интерфейса Robin
echo ============================================================
echo.

echo Остановка старых процессов...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Запуск сервера...
start "Robin Web UI" cmd /k "python -m streamlit run ui.py --server.port 8501 --server.address localhost"

timeout /t 3 /nobreak >nul

echo.
echo ============================================================
echo Сервер запущен!
echo.
echo Откройте в браузере: http://localhost:8501
echo ============================================================
echo.
pause


