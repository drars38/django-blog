FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV SECRET_KEY=build-secret \
    DEBUG=0 \
    ALLOWED_HOSTS=*

# Собираем статические файлы во время сборки, чтобы nginx мог их отдавать
RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]


