# 🚀 Быстрый старт CI/CD

## Что у вас есть

✅ **Django Blog Application** - полнофункциональное веб-приложение  
✅ **Автотесты** - 20 тестов покрывающих весь функционал  
✅ **CI/CD конфигурация** - Jenkinsfile для автоматизации  
✅ **Docker поддержка** - для контейнеризации  
✅ **Документация** - подробные инструкции по настройке  

## 🎯 Задачи лабораторной работы

### 1. GitHub репозиторий ✅
- [x] Создать репозиторий с проектом
- [x] Настроить 3 ветки: main, dev, feature
- [x] Добавить CI/CD конфигурацию

### 2. Jenkins настройка
- [ ] Установить Jenkins
- [ ] Настроить плагины
- [ ] Создать Job для CI/CD
- [ ] Настроить webhook

### 3. Демонстрация CI/CD
- [ ] Показать автоматический запуск тестов
- [ ] Продемонстрировать уведомления
- [ ] Показать процесс слияния веток

## ⚡ Быстрый запуск

### 1. Локальный запуск приложения

```bash
# Перейдите в папку проекта
cd myproject

# Установите зависимости
pip install -r requirements.txt

# Выполните миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser

# Запустите сервер
python manage.py runserver
```

### 2. Запуск тестов

```bash
# Запуск всех тестов
python manage.py test

# Запуск с подробным выводом
python manage.py test --verbosity=2

# Запуск конкретного теста
python manage.py test blog.tests.PostModelTest
```

### 3. Демонстрация CI/CD

```bash
# Запустите демонстрационный скрипт
python demo_ci_cd.py
```

## 📋 Пошаговая настройка

### Шаг 1: GitHub репозиторий

1. Создайте репозиторий на GitHub
2. Подключите локальный проект:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/django-blog-ci-cd.git
   git push -u origin main
   ```
3. Создайте ветки:
   ```bash
   git checkout -b dev
   git push -u origin dev
   git checkout -b feature
   git push -u origin feature
   ```

### Шаг 2: Jenkins установка

**Windows:**
1. Скачайте Jenkins с https://www.jenkins.io/download/
2. Установите .msi файл
3. Откройте http://localhost:8080
4. Получите пароль из `C:\Program Files (x86)\Jenkins\secrets\initialAdminPassword`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install openjdk-11-jdk
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
echo deb https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list
sudo apt update
sudo apt install jenkins
sudo systemctl start jenkins
```

### Шаг 3: Настройка Jenkins Job

1. Установите плагины:
   - Git Plugin
   - GitHub Plugin
   - Pipeline Plugin
   - Email Extension Plugin

2. Создайте Pipeline Job:
   - **Name**: `django-blog-ci-cd`
   - **Type**: Pipeline
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/django-blog-ci-cd.git`
   - **Script Path**: `Jenkinsfile`

### Шаг 4: Настройка Webhook

1. В GitHub репозитории: **Settings > Webhooks**
2. **Payload URL**: `http://YOUR_JENKINS_URL/github-webhook/`
3. **Content type**: `application/json`
4. **Events**: Just the push event

## 🧪 Тестирование CI/CD

### Тест 1: Push в feature ветку
```bash
git checkout feature
# Внесите изменения в код
git add .
git commit -m "Test CI/CD: add new feature"
git push origin feature
# Jenkins должен автоматически запуститься
```

### Тест 2: Создание Pull Request
1. Создайте PR из feature в dev
2. Jenkins должен запуститься автоматически
3. Проверьте результаты в Jenkins UI

### Тест 3: Merge в main
1. После успешных проверок слейте PR
2. Jenkins должен запустить полный цикл CI/CD

## 📊 Мониторинг

### Jenkins Dashboard
- **URL**: http://localhost:8080
- **Jobs**: Список всех задач
- **Build History**: История сборок
- **Console Output**: Детальные логи

### GitHub Integration
- **Status Checks**: Статус проверок в PR
- **Webhooks**: Логи webhook событий
- **Actions**: GitHub Actions (если используется)

## 🔧 Troubleshooting

### Частые проблемы

1. **Jenkins не запускается**
   - Проверьте Java: `java -version`
   - Проверьте порт 8080: `netstat -an | findstr 8080`
   - Перезапустите Jenkins service

2. **Webhook не работает**
   - Проверьте URL webhook
   - Убедитесь что Jenkins доступен
   - Проверьте логи в GitHub

3. **Тесты не проходят**
   - Проверьте Python и зависимости
   - Запустите тесты локально
   - Проверьте логи в Jenkins

### Полезные команды

```bash
# Проверка статуса Jenkins (Linux)
sudo systemctl status jenkins

# Перезапуск Jenkins (Linux)
sudo systemctl restart jenkins

# Логи Jenkins (Linux)
sudo tail -f /var/log/jenkins/jenkins.log

# Проверка портов
netstat -tulpn | grep 8080
```

## 📚 Дополнительные ресурсы

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Docker Documentation](https://docs.docker.com/)

## 🎉 Готово!

Теперь у вас есть полнофункциональная система CI/CD для Django приложения!

**Что дальше:**
1. Настройте Jenkins согласно инструкциям
2. Создайте GitHub репозиторий
3. Продемонстрируйте работу CI/CD
4. Покажите результаты преподавателю

**Удачи с лабораторной работой! 🚀**

