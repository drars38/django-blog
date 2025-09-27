# Настройка GitHub репозитория

## Создание репозитория на GitHub

### 1. Создание нового репозитория

1. Войдите в свой аккаунт GitHub
2. Нажмите кнопку **"New"** или **"+"** в правом верхнем углу
3. Выберите **"New repository"**
4. Заполните форму:
   - **Repository name**: `django-blog-ci-cd`
   - **Description**: `Django Blog Application with CI/CD Pipeline`
   - **Visibility**: Public (или Private по желанию)
   - **Initialize with README**: ❌ (у нас уже есть README)
   - **Add .gitignore**: ❌ (у нас уже есть .gitignore)
   - **Choose a license**: MIT License (опционально)

### 2. Подключение локального репозитория к GitHub

```bash
# Добавляем remote origin
git remote add origin https://github.com/YOUR_USERNAME/django-blog-ci-cd.git

# Переименовываем ветку в main (если нужно)
git branch -M main

# Отправляем код в GitHub
git push -u origin main
```

### 3. Создание веток

```bash
# Создаем и переключаемся на dev ветку
git checkout -b dev
git push -u origin dev

# Создаем и переключаемся на feature ветку
git checkout -b feature
git push -u origin feature

# Возвращаемся на main
git checkout main
```

## Настройка веток

### Main ветка (Production)
- **Назначение**: Стабильная версия для продакшена
- **Защита**: Требует Pull Request для изменений
- **CI/CD**: Полный цикл тестирования и развертывания

### Dev ветка (Development)
- **Назначение**: Разработка новых функций
- **Защита**: Может быть изменена напрямую
- **CI/CD**: Тестирование и предварительная проверка

### Feature ветка (Feature Development)
- **Назначение**: Разработка отдельных функций
- **Защита**: Может быть изменена напрямую
- **CI/CD**: Базовое тестирование

## Настройка защиты веток

### 1. Защита main ветки

1. Перейдите в **Settings > Branches**
2. Нажмите **Add rule**
3. **Branch name pattern**: `main`
4. Включите опции:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Restrict pushes that create files**
5. Нажмите **Create**

### 2. Настройка статусных проверок

1. В настройках защиты ветки main
2. **Status checks that are required**:
   - Выберите Jenkins job для проверки
   - Например: `django-blog-ci-cd`

## Настройка Webhook для Jenkins

### 1. Создание Personal Access Token

1. Перейдите в **Settings > Developer settings > Personal access tokens**
2. Нажмите **Generate new token**
3. Выберите **classic token**
4. **Note**: `Jenkins CI/CD`
5. **Expiration**: `No expiration` (или по желанию)
6. **Scopes**: Выберите:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `admin:repo_hook` (Full control of repository hooks)
7. Нажмите **Generate token**
8. **СОХРАНИТЕ ТОКЕН** - он больше не будет показан!

### 2. Настройка Webhook

1. Перейдите в **Settings > Webhooks**
2. Нажмите **Add webhook**
3. **Payload URL**: `http://YOUR_JENKINS_URL/github-webhook/`
4. **Content type**: `application/json`
5. **Secret**: (оставьте пустым или добавьте секрет)
6. **Events**: Выберите:
   - ✅ **Just the push event**
   - ✅ **Pull requests** (опционально)
7. **Active**: ✅
8. Нажмите **Add webhook**

## Настройка Jenkins для работы с GitHub

### 1. Добавление GitHub credentials

1. В Jenkins перейдите в **Manage Jenkins > Manage Credentials**
2. Выберите **System > Global credentials**
3. Нажмите **Add Credentials**
4. **Kind**: `Username with password`
5. **Username**: ваш GitHub username
6. **Password**: Personal Access Token (не пароль!)
7. **ID**: `github-token`
8. **Description**: `GitHub Personal Access Token`

### 2. Настройка GitHub Server

1. Перейдите в **Manage Jenkins > Configure System**
2. Найдите раздел **GitHub**
3. **GitHub Servers**:
   - **Name**: `GitHub`
   - **Server URL**: `https://api.github.com`
   - **Credentials**: выберите созданный токен
4. Нажмите **Test connection** - должно показать "Success"

## Workflow для разработки

### 1. Разработка новой функции

```bash
# Создаем новую ветку от dev
git checkout dev
git pull origin dev
git checkout -b feature/new-feature

# Разрабатываем функцию
# ... делаем изменения ...

# Коммитим изменения
git add .
git commit -m "Add new feature: description"

# Отправляем в GitHub
git push -u origin feature/new-feature

# Создаем Pull Request в GitHub UI
```

### 2. Слияние в dev

```bash
# После одобрения PR, сливаем в dev
git checkout dev
git pull origin dev
git merge feature/new-feature
git push origin dev

# Удаляем feature ветку
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 3. Релиз в main

```bash
# Создаем Pull Request из dev в main
# После одобрения и прохождения всех проверок:
git checkout main
git pull origin main
git merge dev
git push origin main

# Создаем тег релиза
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Мониторинг и уведомления

### 1. Настройка уведомлений

- **Email**: Настройте в Jenkins для отправки уведомлений
- **GitHub**: Автоматические уведомления о статусе проверок
- **Slack/Discord**: Можно настроить через плагины Jenkins

### 2. Дашборд

- **GitHub**: Просмотр статуса проверок в PR
- **Jenkins**: Blue Ocean для визуализации pipeline
- **GitHub Actions**: Альтернатива Jenkins (опционально)

## Troubleshooting

### Частые проблемы

1. **Webhook не срабатывает**
   - Проверьте URL webhook
   - Убедитесь что Jenkins доступен
   - Проверьте логи webhook в GitHub

2. **Ошибки аутентификации**
   - Проверьте Personal Access Token
   - Убедитесь что токен имеет нужные права
   - Проверьте настройки credentials в Jenkins

3. **Проблемы с правами доступа**
   - Убедитесь что токен имеет права на репозиторий
   - Проверьте настройки репозитория (public/private)

### Полезные ссылки

- [GitHub Webhooks Documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks)
- [Jenkins GitHub Plugin](https://plugins.jenkins.io/github/)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

