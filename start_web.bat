@echo off
chcp 65001 >nul
echo ============================================================
echo Запуск веб-интерфейса Robin
echo ============================================================
echo.
echo Веб-интерфейс будет доступен по адресу:
echo   http://localhost:8501
echo.
echo Нажмите Ctrl+C для остановки
echo ============================================================
echo.

python -m streamlit run ui.py --server.port 8501 --server.address localhost

pause


