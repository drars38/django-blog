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
    }
    
    post {
        always {
            echo 'Сборка завершена'
            archiveArtifacts artifacts: 'build_info.txt', fingerprint: true
        }
        success {
            echo 'Сборка прошла успешно!'
            emailext (
                subject: "✅ Успешная сборка: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Сборка ${env.BUILD_NUMBER} в проекте ${env.JOB_NAME} прошла успешно.\nВетка: ${env.BRANCH_NAME}\nКоммит: ${env.GIT_COMMIT}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
        failure {
            echo 'Сборка завершилась с ошибкой!'
            emailext (
                subject: "❌ Ошибка сборки: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Сборка ${env.BUILD_NUMBER} в проекте ${env.JOB_NAME} завершилась с ошибкой.\nВетка: ${env.BRANCH_NAME}\nКоммит: ${env.GIT_COMMIT}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
