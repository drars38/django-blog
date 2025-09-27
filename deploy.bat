@echo off
REM Скрипт автоматического развертывания Django приложения для Windows

echo 🚀 Начинаем развертывание Django Blog Application...

REM Проверяем наличие Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Установите Python 3.8+
    pause
    exit /b 1
)

REM Проверяем наличие pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip не найден. Установите pip
    pause
    exit /b 1
)

echo ✅ Python и pip найдены

REM Создаем виртуальное окружение
echo 📦 Создаем виртуальное окружение...
python -m venv venv

REM Активируем виртуальное окружение
echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate.bat

REM Устанавливаем зависимости
echo 📚 Устанавливаем зависимости...
pip install -r requirements.txt

REM Выполняем миграции
echo 🗄️ Выполняем миграции базы данных...
python manage.py makemigrations
python manage.py migrate

REM Создаем суперпользователя (если не существует)
echo 👤 Создаем суперпользователя...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Суперпользователь уже существует')"

REM Собираем статические файлы
echo 📁 Собираем статические файлы...
python manage.py collectstatic --noinput

REM Запускаем тесты
echo 🧪 Запускаем тесты...
python manage.py test

if %errorlevel% equ 0 (
    echo ✅ Все тесты прошли успешно!
    echo 🎉 Развертывание завершено успешно!
    echo 🌐 Запустите сервер командой: python manage.py runserver
    echo 🔗 Откройте http://127.0.0.1:8000 в браузере
    echo 👤 Админ панель: http://127.0.0.1:8000/admin (admin/admin123)
) else (
    echo ❌ Некоторые тесты не прошли. Проверьте код.
    pause
    exit /b 1
)

pause
