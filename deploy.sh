#!/bin/bash

# Скрипт автоматического развертывания Django приложения

echo "🚀 Начинаем развертывание Django Blog Application..."

# Проверяем наличие Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не найден. Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip не найден. Установите pip"
    exit 1
fi

echo "✅ Python и pip найдены"

# Создаем виртуальное окружение
echo "📦 Создаем виртуальное окружение..."
python -m venv venv

# Активируем виртуальное окружение
echo "🔧 Активируем виртуальное окружение..."
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Устанавливаем зависимости
echo "📚 Устанавливаем зависимости..."
pip install -r requirements.txt

# Выполняем миграции
echo "🗄️ Выполняем миграции базы данных..."
python manage.py makemigrations
python manage.py migrate

# Создаем суперпользователя (если не существует)
echo "👤 Создаем суперпользователя..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан: admin/admin123')
else:
    print('Суперпользователь уже существует')
"

# Собираем статические файлы
echo "📁 Собираем статические файлы..."
python manage.py collectstatic --noinput

# Запускаем тесты
echo "🧪 Запускаем тесты..."
python manage.py test

if [ $? -eq 0 ]; then
    echo "✅ Все тесты прошли успешно!"
    echo "🎉 Развертывание завершено успешно!"
    echo "🌐 Запустите сервер командой: python manage.py runserver"
    echo "🔗 Откройте http://127.0.0.1:8000 в браузере"
    echo "👤 Админ панель: http://127.0.0.1:8000/admin (admin/admin123)"
else
    echo "❌ Некоторые тесты не прошли. Проверьте код."
    exit 1
fi

