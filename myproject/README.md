## Запуск в Docker

1. Создайте файл `.env` на основе `.env.sample`:
   - Отредактируйте `POSTGRES_*`, `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`.

2. Запустите сервисы:

```bash
docker compose -f myproject/docker-compose.yml up -d --build
```

Приложение будет доступно на `http://localhost/` (через `nginx`).

## CI/CD (GitHub Actions + GHCR)

- Workflow: `.github/workflows/ci.yml`
- Пушит образ `ghcr.io/<owner>/myproject-web` с тегами ветки, `latest` (для дефолтной ветки) и `sha`.
- Для работы достаточно репозитория в GitHub (доступ к `ghcr` через `GITHUB_TOKEN`).

## Полезные команды

- Логи веб-приложения:

```bash
docker logs -f myproject-web
```

- Остановка и удаление:

```bash
docker compose -f myproject/docker-compose.yml down -v
```






