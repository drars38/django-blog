@echo off
echo 🚀 Запуск Jenkins с webhook для GitHub
echo =====================================

REM Проверяем, установлен ли ngrok
if not exist "C:\ngrok\ngrok.exe" (
    echo ❌ ngrok не найден в C:\ngrok\
    echo Запустите setup_ngrok.bat для установки
    pause
    exit /b 1
)

REM Проверяем, запущен ли Jenkins
echo 🔍 Проверяем Jenkins...
curl -s http://localhost:8080 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Jenkins не запущен на порту 8080
    echo 🚀 Запускаем Jenkins...
    echo Откройте http://localhost:8080 в браузере
    echo Настройте Jenkins согласно инструкции
) else (
    echo ✅ Jenkins уже запущен
)

REM Запускаем ngrok
echo 🌐 Запускаем ngrok туннель...
echo 📋 Скопируйте URL из ngrok для настройки webhook в GitHub
echo.
start "ngrok" cmd /k "C:\ngrok\ngrok.exe http 8080"

echo.
echo ✅ Jenkins и ngrok запущены!
echo.
echo 📋 Следующие шаги:
echo 1. Скопируйте URL из окна ngrok (например: https://abc123.ngrok.io)
echo 2. В GitHub репозитории: Settings > Webhooks
echo 3. Payload URL: https://abc123.ngrok.io/github-webhook/
echo 4. Content type: application/json
echo 5. Events: Just the push event
echo.
echo 🔗 Jenkins доступен по адресу: http://localhost:8080
echo 🌐 Публичный URL будет показан в окне ngrok
echo.
echo 📚 Подробная инструкция в JENKINS_SETUP.md
echo.
pause

