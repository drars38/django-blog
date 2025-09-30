# Руководство по деплою Django Blog Application

## 🚀 Обзор процесса деплоя

Наш CI/CD pipeline теперь включает автоматический деплой для разных окружений:

### 🌿 Ветки и окружения

| Ветка | Окружение | Порт | База данных | Админ |
|-------|-----------|------|-------------|-------|
| `feature` | Тестирование | - | - | - |
| `dev` | Development | 8001 | blog_dev_db | dev_admin/dev123 |
| `main` | Production | 8000 | blog_db | admin/admin123 |

## 🔄 Workflow деплоя

### 1. Разработка (Feature ветка)
```bash
# Создаем feature ветку
git checkout dev
git pull origin dev
git checkout -b feature/new-feature

# Разрабатываем функцию
# ... делаем изменения ...

# Коммитим и пушим
git add .
git commit -m "Add new feature: description"
git push -u origin feature/new-feature

# Создаем Pull Request в GitHub
```

### 2. Деплой в Development
- При push в `dev` ветку Jenkins автоматически:
  - ✅ Запускает тесты
  - ✅ Проверяет качество кода
  - ✅ Деплоит в dev окружение (порт 8001)
  - ✅ Проверяет здоровье приложения
  - ✅ Отправляет уведомления

**Доступ к dev окружению:**
- URL: http://localhost:8001
- Админ: dev_admin / dev123
- База данных: PostgreSQL на порту 5433

### 3. Деплой в Production
- При push в `main` ветку Jenkins автоматически:
  - ✅ Запускает полный цикл тестирования
  - ✅ Деплоит в production окружение (порт 8000)
  - ✅ Проверяет здоровье приложения
  - ✅ Отправляет уведомления

**Доступ к production окружению:**
- URL: http://localhost:8000
- Админ: admin / admin123
- База данных: PostgreSQL на порту 5432

## 🐳 Docker конфигурация

### Development (docker-compose.dev.yml)
```yaml
services:
  web:
    ports:
      - "8001:8000"
    environment:
      - DEBUG=True
  db:
    ports:
      - "5433:5432"
    environment:
      POSTGRES_DB: blog_dev_db
```

### Production (docker-compose.yml)
```yaml
services:
  web:
    ports:
      - "8000:8000"
  db:
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: blog_db
```

## 📧 Уведомления

### Успешный деплой
- **Тема**: ✅ Успешная сборка и деплой
- **Содержание**: Информация о ветке, коммите, URL приложения и учетных данных

### Ошибка деплоя
- **Тема**: ❌ Ошибка сборки/деплоя
- **Содержание**: Детали ошибки и ссылка на логи Jenkins

## 🔧 Ручной деплой

### Development
```bash
# Остановить dev контейнеры
docker-compose -f docker-compose.dev.yml down

# Запустить dev окружение
docker-compose -f docker-compose.dev.yml up -d

# Выполнить миграции
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Создать суперпользователя
docker-compose -f docker-compose.dev.yml exec web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('dev_admin', 'dev@example.com', 'dev123')"
```

### Production
```bash
# Остановить production контейнеры
docker-compose down

# Запустить production окружение
docker-compose up -d

# Выполнить миграции
docker-compose exec web python manage.py migrate

# Создать суперпользователя
docker-compose exec web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```

## 🏥 Health Check

Pipeline автоматически проверяет здоровье приложения:
- **Попытки**: 5 попыток с интервалом 10 секунд
- **Метод**: HTTP запрос к корневому URL
- **Результат**: UNSTABLE если приложение не отвечает

## 🚨 Откат (Rollback)

При ошибке деплоя Jenkins автоматически:
1. Останавливает новые контейнеры
2. Запускает предыдущую версию
3. Отправляет уведомление об ошибке

## 📊 Мониторинг

### Логи Jenkins
- **Console Output**: Детальные логи выполнения
- **Build Artifacts**: build_info.txt с информацией о сборке

### Docker контейнеры
```bash
# Проверить статус dev
docker-compose -f docker-compose.dev.yml ps

# Проверить статус production
docker-compose ps

# Логи dev
docker-compose -f docker-compose.dev.yml logs -f web

# Логи production
docker-compose logs -f web
```

## 🔍 Troubleshooting

### Частые проблемы

1. **Порт уже используется**
   ```bash
   # Найти процесс на порту
   netstat -ano | findstr :8000
   # Убить процесс
   taskkill /PID <PID> /F
   ```

2. **Docker контейнеры не запускаются**
   ```bash
   # Очистить все контейнеры
   docker-compose down --remove-orphans
   docker system prune -f
   # Перезапустить
   docker-compose up -d
   ```

3. **Ошибки миграций**
   ```bash
   # Сбросить миграции
   docker-compose exec web python manage.py migrate --fake-initial
   ```

4. **Проблемы с правами доступа**
   ```bash
   # Проверить права на файлы
   icacls . /grant Everyone:F /T
   ```

### Полезные команды

```bash
# Перезапустить все сервисы
docker-compose restart

# Пересобрать образы
docker-compose build --no-cache

# Очистить неиспользуемые образы
docker image prune -f

# Просмотр логов в реальном времени
docker-compose logs -f
```

## 📝 Лучшие практики

1. **Всегда тестируйте в dev** перед деплоем в production
2. **Проверяйте уведомления** о статусе деплоя
3. **Мониторьте логи** при возникновении проблем
4. **Делайте бэкапы** базы данных перед крупными изменениями
5. **Используйте теги** для версионирования релизов

## 🎯 Следующие шаги

- [ ] Настроить мониторинг производительности
- [ ] Добавить автоматическое создание бэкапов
- [ ] Настроить SSL сертификаты
- [ ] Добавить load balancing
- [ ] Настроить мониторинг логов (ELK Stack)

