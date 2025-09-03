@echo off
echo Iniciando servidor Django...
echo.
echo El servidor estara disponible en: http://127.0.0.1:8000
echo.
echo Para detener el servidor, presiona Ctrl+C
echo.
python manage.py runserver 127.0.0.1:8000
pause
