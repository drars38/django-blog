pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    triggers {
        // Требуется установленный GitHub plugin и настроенный webhook на Jenkins
        githubPush()
    }

    environment {
        DJANGO_SETTINGS_MODULE = 'myproject.settings'
        PYTHONPATH = "${WORKSPACE}"
        // ВАЖНО: добавьте креденшлы в Jenkins и укажите их ID здесь
        GITHUB_CREDENTIALS_ID = 'github-token1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat 'git status'
            }
        }

        stage('Setup Python') {
            steps {
                bat '''
                    python --version
                    pip --version
                '''
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Migrate (SQLite)') {
            steps {
                bat '''
                    python manage.py makemigrations --noinput
                    python manage.py migrate --noinput
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                    python manage.py test --verbosity=2
                '''
            }
        }

        stage('Merge dev -> main (on success)') {
            when {
                expression {
                    // Сравниваем SHA HEAD и origin/dev, работает в detached HEAD
                    def headSha = bat(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    def devSha  = bat(script: 'git rev-parse origin/dev', returnStdout: true).trim()
                    echo "HEAD=${headSha} | origin/dev=${devSha}"
                    return headSha == devSha
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: GITHUB_CREDENTIALS_ID, usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
                    bat '''
                        setlocal enableextensions enabledelayedexpansion
                        git config user.name "Jenkins CI"
                        git config user.email "ci@example.local"

                        rem Получаем origin URL
                        for /f "delims=" %%i in ('git remote get-url origin') do set ORIGIN_URL=%%i
                        echo Origin: !ORIGIN_URL!

                        rem Строим URL с авторизацией для push
                        set AUTH_URL=!ORIGIN_URL:https://=https://%GIT_USERNAME%:%GIT_TOKEN%@!

                        rem Обновляем refs
                        git fetch origin +refs/heads/*:refs/remotes/origin/*

                        rem Переключаемся на main и подтягиваем актуальное
                        git checkout -B main origin/main
                        git merge --no-ff dev -m "Auto-merge dev into main [Jenkins]"

                        rem Пушим main
                        git push "!AUTH_URL!" main

                        rem Возврат на dev (необязательно)
                        git checkout dev
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Сборка прошла успешно'
        }
        failure {
            echo '❌ Ошибка сборки'
        }
        always {
            echo "Готово: ${currentBuild.currentResult}"
        }
    }
}


