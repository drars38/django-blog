@echo off
echo 🚀 Установка ngrok для Jenkins webhook
echo =====================================

REM Создаем папку для ngrok
if not exist "C:\ngrok" mkdir "C:\ngrok"
cd /d "C:\ngrok"

echo 📥 Скачиваем ngrok...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo 📦 Распаковываем ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo 🗑️ Удаляем zip файл...
del ngrok.zip

echo ✅ ngrok установлен в C:\ngrok\
echo.
echo 🔑 Настройка токена:
echo 1. Зайдите на https://dashboard.ngrok.com/
echo 2. Войдите в аккаунт (регистрация бесплатная)
echo 3. Скопируйте ваш authtoken
echo 4. Запустите: C:\ngrok\ngrok.exe authtoken YOUR_TOKEN
echo.
echo 🚀 Для запуска туннеля к Jenkins:
echo C:\ngrok\ngrok.exe http 8080
echo.
echo 📋 Полученный URL используйте для webhook в GitHub
echo.
pause

