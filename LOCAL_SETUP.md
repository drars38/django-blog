# 🏠 Локальная настройка CI/CD

## 🎯 Варианты локальной настройки

### **Вариант 1: GitHub Actions (Рекомендуется)**
- ✅ Встроенная CI/CD система GitHub
- ✅ Не требует дополнительного ПО
- ✅ Работает автоматически при push
- ✅ Бесплатно для публичных репозиториев

### **Вариант 2: Локальный Jenkins**
- ✅ Полный контроль над процессом
- ✅ Можно настроить сложные pipeline
- ⚠️ Требует установки Jenkins
- ⚠️ Нужен ngrok для webhook

### **Вариант 3: Симуляция CI/CD**
- ✅ Простота настройки
- ✅ Работает без интернета
- ✅ Подходит для демонстрации
- ⚠️ Не автоматизировано

## 🚀 Вариант 1: GitHub Actions

### Шаг 1: Создайте GitHub репозиторий
```bash
# В папке myproject
git init
git add .
git commit -m "Initial commit with CI/CD"

# Создайте репозиторий на GitHub
git remote add origin https://github.com/YOUR_USERNAME/django-blog-ci-cd.git
git push -u origin main
```

### Шаг 2: GitHub Actions автоматически запустится
- При push в любую ветку (main, dev, feature)
- При создании Pull Request
- Проверит код на 3 версиях Python (3.9, 3.10, 3.11)
- Запустит все тесты
- Создаст артефакты сборки

### Шаг 3: Просмотр результатов
1. Перейдите в GitHub репозиторий
2. Вкладка **Actions**
3. Выберите workflow run
4. Просмотрите детальные логи

## 🏠 Вариант 2: Локальный Jenkins

### Установка Jenkins
```bash
# Windows
# Скачайте с https://www.jenkins.io/download/
# Установите .msi файл

# Linux
sudo apt update
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
echo deb https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt update
sudo apt install jenkins
sudo systemctl start jenkins
```

### Настройка Jenkins Job
1. Откройте http://localhost:8080
2. Создайте Pipeline Job
3. Используйте Jenkinsfile из проекта
4. Настройте webhook (потребуется ngrok)

## 🎭 Вариант 3: Симуляция CI/CD

### Запуск симуляции
```bash
# Windows
simulate_ci_cd.bat

# Linux/Mac
chmod +x simulate_ci_cd.sh
./simulate_ci_cd.sh
```

### Что делает симуляция:
1. ✅ Проверка синтаксиса кода
2. ✅ Установка зависимостей
3. ✅ Настройка базы данных
4. ✅ Запуск автотестов
5. ✅ Проверка качества кода
6. ✅ Сборка приложения
7. ✅ Уведомления команде

## 📊 Сравнение вариантов

| Критерий | GitHub Actions | Локальный Jenkins | Симуляция |
|----------|----------------|-------------------|-----------|
| Сложность настройки | 🟢 Низкая | 🟡 Средняя | 🟢 Очень низкая |
| Автоматизация | 🟢 Полная | 🟢 Полная | 🔴 Ручная |
| Требования | 🟢 Только GitHub | 🟡 Jenkins + ngrok | 🟢 Только Python |
| Стоимость | 🟢 Бесплатно | 🟢 Бесплатно | 🟢 Бесплатно |
| Надежность | 🟢 Высокая | 🟡 Средняя | 🟡 Средняя |
| Масштабируемость | 🟢 Высокая | 🟡 Ограниченная | 🔴 Низкая |

## 🎯 Рекомендация для лабораторной работы

### **Для демонстрации преподавателю:**
1. **GitHub Actions** - покажите автоматический запуск при push
2. **Симуляция** - покажите локальный процесс
3. **Jenkins** - если есть время и желание

### **Пошаговый план демонстрации:**

#### Шаг 1: GitHub Actions
```bash
# Создайте репозиторий и отправьте код
git push origin main

# Покажите в GitHub:
# - Вкладка Actions
# - Запуск workflow
# - Результаты тестов
# - Артефакты сборки
```

#### Шаг 2: Локальная симуляция
```bash
# Запустите симуляцию
simulate_ci_cd.bat

# Покажите:
# - Поэтапное выполнение
# - Результаты тестов
# - Сборку приложения
```

#### Шаг 3: Демонстрация процесса
```bash
# Запустите демо скрипт
python demo_ci_cd.py

# Покажите:
# - Полный workflow
# - Преимущества CI/CD
# - Интеграцию компонентов
```

## 🔧 Troubleshooting

### GitHub Actions не запускается
- Проверьте, что файл `.github/workflows/ci-cd.yml` в репозитории
- Убедитесь, что синтаксис YAML корректен
- Проверьте права доступа к репозиторию

### Локальные тесты не проходят
- Убедитесь, что Python и Django установлены
- Проверьте, что база данных настроена
- Запустите `python manage.py test` для диагностики

### Jenkins не запускается
- Проверьте, что Java установлена
- Убедитесь, что порт 8080 свободен
- Проверьте логи Jenkins

## 📚 Дополнительные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)

## 🎉 Готово!

Теперь у вас есть 3 варианта настройки CI/CD:
1. **GitHub Actions** - для автоматизации
2. **Локальный Jenkins** - для полного контроля
3. **Симуляция** - для демонстрации

Выберите подходящий вариант для вашей лабораторной работы!
