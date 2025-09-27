# Настройка Jenkins для CI/CD

## Установка Jenkins

### Windows

1. **Скачайте Jenkins:**
   - Перейдите на https://www.jenkins.io/download/
   - Скачайте Jenkins для Windows

2. **Установите Jenkins:**
   - Запустите скачанный .msi файл
   - Следуйте инструкциям установщика
   - Jenkins будет установлен как Windows Service

3. **Запустите Jenkins:**
   - Откройте браузер и перейдите на http://localhost:8080
   - Получите initial admin password из файла:
     ```
     C:\Program Files (x86)\Jenkins\secrets\initialAdminPassword
     ```

### Linux (Ubuntu/Debian)

```bash
# Обновляем пакеты
sudo apt update

# Устанавливаем Java (требуется для Jenkins)
sudo apt install openjdk-11-jdk

# Добавляем ключ репозитория Jenkins
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -

# Добавляем репозиторий Jenkins
echo deb https://pkg.jenkins.io/debian binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list

# Обновляем пакеты и устанавливаем Jenkins
sudo apt update
sudo apt install jenkins

# Запускаем Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Проверяем статус
sudo systemctl status jenkins
```

## Настройка Jenkins

### 1. Первоначальная настройка

1. Откройте http://localhost:8080 в браузере
2. Введите initial admin password
3. Выберите "Install suggested plugins"
4. Создайте admin пользователя
5. Настройте URL Jenkins (по умолчанию http://localhost:8080/)

### 2. Установка необходимых плагинов

Перейдите в **Manage Jenkins > Manage Plugins** и установите:

- **Git Plugin** - для работы с Git репозиториями
- **GitHub Plugin** - для интеграции с GitHub
- **Pipeline Plugin** - для Pipeline as Code
- **Email Extension Plugin** - для отправки уведомлений
- **Build Timeout Plugin** - для контроля времени сборки
- **Workspace Cleanup Plugin** - для очистки workspace

### 3. Настройка глобальных инструментов

Перейдите в **Manage Jenkins > Global Tool Configuration**:

- **JDK**: Укажите путь к Java (обычно автоматически определяется)
- **Git**: Укажите путь к Git (обычно автоматически определяется)
- **Python**: Добавьте Python installation:
  - Name: `Python-3.11`
  - Install automatically: ✅
  - Version: `3.11.x`

## Создание Jenkins Job

### 1. Создание Pipeline Job

1. Нажмите **New Item**
2. Введите имя: `django-blog-ci-cd`
3. Выберите **Pipeline**
4. Нажмите **OK**

### 2. Настройка Pipeline

В разделе **Pipeline**:

- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: `https://github.com/YOUR_USERNAME/django-blog.git`
- **Credentials**: Добавьте GitHub credentials если репозиторий приватный
- **Branch Specifier**: `*/main` (для main ветки)
- **Script Path**: `Jenkinsfile`

### 3. Настройка Webhook (GitHub)

1. Перейдите в настройки вашего GitHub репозитория
2. Выберите **Settings > Webhooks**
3. Нажмите **Add webhook**
4. **Payload URL**: `http://YOUR_JENKINS_URL/github-webhook/`
5. **Content type**: `application/json`
6. **Events**: Выберите "Just the push event"
7. Нажмите **Add webhook**

### 4. Настройка уведомлений по email

1. Перейдите в **Manage Jenkins > Configure System**
2. В разделе **E-mail Notification**:
   - **SMTP server**: smtp.gmail.com (для Gmail)
   - **Default user e-mail suffix**: @gmail.com
   - **Use SMTP Authentication**: ✅
   - **User Name**: ваш email
   - **Password**: пароль приложения
   - **Use SSL**: ✅
   - **SMTP Port**: 465

## Настройка для разных веток

### Job для main ветки (Production)
- **Branch Specifier**: `*/main`
- **Pipeline Script Path**: `Jenkinsfile`

### Job для dev ветки (Development)
- **Branch Specifier**: `*/dev`
- **Pipeline Script Path**: `Jenkinsfile`

### Job для feature ветки (Feature Testing)
- **Branch Specifier**: `*/feature`
- **Pipeline Script Path**: `Jenkinsfile`

## Запуск тестов

### Ручной запуск
1. Перейдите в ваш Job
2. Нажмите **Build Now**

### Автоматический запуск
- При push в соответствующую ветку
- Webhook автоматически запустит сборку

## Мониторинг

### Просмотр результатов
- **Console Output**: детальный лог выполнения
- **Test Results**: результаты тестов
- **Build Artifacts**: собранные артефакты

### Уведомления
- Email при успешной/неуспешной сборке
- Уведомления в Jenkins UI

## Troubleshooting

### Частые проблемы

1. **Git не найден**
   - Установите Git и добавьте в PATH
   - Перезапустите Jenkins

2. **Python не найден**
   - Установите Python
   - Настройте в Global Tool Configuration

3. **Права доступа**
   - Убедитесь что Jenkins имеет права на workspace
   - Проверьте права на файлы проекта

4. **Webhook не работает**
   - Проверьте URL webhook
   - Убедитесь что Jenkins доступен извне
   - Проверьте логи GitHub webhook

### Логи
- **Jenkins logs**: `/var/log/jenkins/jenkins.log` (Linux) или в Windows Service
- **Job logs**: Console Output в Jenkins UI

