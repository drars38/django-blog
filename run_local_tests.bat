@echo off
echo 🧪 Локальный запуск тестов CI/CD
echo ================================

echo 📋 Проверяем окружение...
python --version
pip --version

echo.
echo 📦 Устанавливаем зависимости...
pip install -r requirements.txt

echo.
echo 🗄️ Настраиваем базу данных...
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo.
echo 🧪 Запускаем тесты...
python manage.py test --verbosity=2

if %errorlevel% equ 0 (
    echo.
    echo ✅ Все тесты прошли успешно!
    echo 🎉 CI/CD pipeline выполнен локально!
) else (
    echo.
    echo ❌ Некоторые тесты не прошли
    echo 🔧 Проверьте ошибки выше
)

echo.
echo 📊 Статистика:
echo - Python: 
python --version
echo - Django:
python -c "import django; print(django.get_version())"
echo - Тесты: Запущены

pause
