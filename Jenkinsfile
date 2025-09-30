pipeline {
    agent any
    
    environment {
        DJANGO_SETTINGS_MODULE = 'myproject.settings'
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Код получен из репозитория'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Настройка Python окружения'
                bat '''
                    python --version
                    pip --version
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Установка зависимостей'
                bat '''
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Database Setup') {
            steps {
                echo 'Настройка базы данных'
                bat '''
                    python manage.py makemigrations --noinput
                    python manage.py migrate --noinput
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Запуск автотестов'
                bat '''
                    python manage.py test --verbosity=2
                '''
            }
            post {
                always {
                    echo 'Тестирование завершено'
                }
                success {
                    echo 'Все тесты прошли успешно!'
                }
                failure {
                    echo 'Некоторые тесты не прошли'
                }
            }
        }
        
        stage('Code Quality Check') {
            steps {
                echo 'Проверка качества кода'
                bat '''
                    python -m py_compile manage.py
                    python -m py_compile blog/models.py
                    python -m py_compile blog/views.py
                    python -m py_compile blog/tests.py
                '''
            }
        }
        
        stage('Build Documentation') {
            steps {
                echo 'Сборка документации'
                bat '''
                    echo "Документация проекта:" > build_info.txt
                    echo "Проект: Django Blog Application" >> build_info.txt
                    echo "Ветка: ${env.BRANCH_NAME}" >> build_info.txt
                    echo "Коммит: ${env.GIT_COMMIT}" >> build_info.txt
                    echo "Дата сборки: %DATE% %TIME%" >> build_info.txt
                '''
            }
        }
        
        stage('Deploy to Development') {
            when {
                branch 'dev'
            }
            steps {
                echo '🚀 Деплой в Development окружение'
                bat '''
                    echo "Начинаем деплой в dev окружение..."
                    
                    REM Останавливаем предыдущие dev контейнеры
                    docker-compose -f docker-compose.dev.yml down --remove-orphans
                    
                    REM Собираем новый dev образ
                    docker-compose -f docker-compose.dev.yml build --no-cache
                    
                    REM Запускаем dev окружение
                    docker-compose -f docker-compose.dev.yml up -d
                    
                    REM Ждем запуска сервисов
                    timeout /t 10 /nobreak
                    
                    REM Проверяем статус контейнеров
                    docker-compose -f docker-compose.dev.yml ps
                    
                    REM Выполняем миграции в dev
                    docker-compose -f docker-compose.dev.yml exec -T web python manage.py migrate --noinput
                    
                    REM Собираем статические файлы в dev
                    docker-compose -f docker-compose.dev.yml exec -T web python manage.py collectstatic --noinput
                    
                    REM Создаем суперпользователя для dev
                    docker-compose -f docker-compose.dev.yml exec -T web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('dev_admin', 'dev@example.com', 'dev123') if not User.objects.filter(username='dev_admin').exists() else print('Dev суперпользователь уже существует')"
                    
                    echo "✅ Деплой в dev окружение завершен!"
                    echo "🌐 Dev сервер: http://localhost:8001"
                    echo "👤 Dev админ: dev_admin/dev123"
                '''
            }
            post {
                success {
                    echo '✅ Деплой в dev окружение прошел успешно!'
                }
                failure {
                    echo '❌ Ошибка деплоя в dev окружение!'
                    echo 'Откатываем dev изменения...'
                    bat '''
                        docker-compose -f docker-compose.dev.yml down
                        docker-compose -f docker-compose.dev.yml up -d
                    '''
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Деплой в Production окружение'
                bat '''
                    echo "Начинаем деплой в production окружение..."
                    
                    REM Останавливаем предыдущие контейнеры
                    docker-compose down --remove-orphans
                    
                    REM Собираем новый образ
                    docker-compose build --no-cache
                    
                    REM Запускаем production окружение
                    docker-compose up -d
                    
                    REM Ждем запуска сервисов
                    timeout /t 10 /nobreak
                    
                    REM Проверяем статус контейнеров
                    docker-compose ps
                    
                    REM Выполняем миграции в production
                    docker-compose exec -T web python manage.py migrate --noinput
                    
                    REM Собираем статические файлы в production
                    docker-compose exec -T web python manage.py collectstatic --noinput
                    
                    REM Создаем суперпользователя для production
                    docker-compose exec -T web python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Production суперпользователь уже существует')"
                    
                    echo "✅ Деплой в production окружение завершен!"
                    echo "🌐 Production сервер: http://localhost:8000"
                    echo "👤 Production админ: admin/admin123"
                '''
            }
            post {
                success {
                    echo '✅ Деплой в production окружение прошел успешно!'
                }
                failure {
                    echo '❌ Ошибка деплоя в production окружение!'
                    echo 'Откатываем изменения...'
                    bat '''
                        docker-compose down
                        docker-compose up -d
                    '''
                }
            }
        }
        
        stage('Health Check') {
            when {
                anyOf {
                    branch 'main'
                    branch 'dev'
                }
            }
            steps {
                echo '🏥 Проверка здоровья приложения'
                script {
                    def branchName = env.BRANCH_NAME
                    def port = branchName == 'main' ? '8000' : '8001'
                    def maxAttempts = 5
                    def attempt = 1
                    
                    while (attempt <= maxAttempts) {
                        echo "Попытка ${attempt}/${maxAttempts} проверки здоровья на порту ${port}..."
                        
                        // Используем PowerShell для проверки HTTP статуса
                        def result = bat(
                            script: "powershell -Command \"try { $response = Invoke-WebRequest -Uri 'http://localhost:${port}/' -TimeoutSec 10; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }\"",
                            returnStatus: true
                        )
                        
                        if (result == 0) {
                            echo "✅ Приложение здорово и отвечает на порту ${port}"
                            break
                        } else {
                            echo "⏳ Приложение еще не готово, ждем 10 секунд..."
                            sleep(10)
                            attempt++
                        }
                    }
                    
                    if (attempt > maxAttempts) {
                        echo "❌ Приложение не отвечает после ${maxAttempts} попыток"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Сборка завершена'
            archiveArtifacts artifacts: 'build_info.txt', fingerprint: true
        }
        success {
            echo 'Сборка прошла успешно!'
            script {
                def branchName = env.BRANCH_NAME
                def deployInfo = ""
                def serverUrl = ""
                
                if (branchName == 'main') {
                    deployInfo = "✅ Деплой в Production завершен успешно!"
                    serverUrl = "🌐 Production: http://localhost:8000\n👤 Админ: admin/admin123"
                } else if (branchName == 'dev') {
                    deployInfo = "✅ Деплой в Development завершен успешно!"
                    serverUrl = "🌐 Development: http://localhost:8001\n👤 Админ: dev_admin/dev123"
                } else {
                    deployInfo = "✅ Сборка завершена успешно!"
                }
                
                emailext (
                    subject: "✅ Успешная сборка и деплой: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                    body: """Сборка ${env.BUILD_NUMBER} в проекте ${env.JOB_NAME} прошла успешно.
Ветка: ${env.BRANCH_NAME}
Коммит: ${env.GIT_COMMIT}

${deployInfo}
${serverUrl}

Проверьте приложение по указанной ссылке.""",
                    to: "${env.CHANGE_AUTHOR_EMAIL}"
                )
            }
        }
        failure {
            echo 'Сборка завершилась с ошибкой!'
            script {
                def branchName = env.BRANCH_NAME
                def deployInfo = ""
                
                if (branchName == 'main') {
                    deployInfo = "❌ Ошибка деплоя в Production!"
                } else if (branchName == 'dev') {
                    deployInfo = "❌ Ошибка деплоя в Development!"
                } else {
                    deployInfo = "❌ Ошибка сборки!"
                }
                
                emailext (
                    subject: "❌ Ошибка сборки/деплоя: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                    body: """Сборка ${env.BUILD_NUMBER} в проекте ${env.JOB_NAME} завершилась с ошибкой.
Ветка: ${env.BRANCH_NAME}
Коммит: ${env.GIT_COMMIT}

${deployInfo}

Проверьте логи Jenkins для детальной информации об ошибке.""",
                    to: "${env.CHANGE_AUTHOR_EMAIL}"
                )
            }
        }
    }
}

