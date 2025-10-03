pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    parameters {
        booleanParam(name: 'MERGE_TO_MAIN', defaultValue: false, description: 'Включить авто-мердж dev -> main после успешной сборки')
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
                script {
                    try {
                        bat '''
                            python manage.py test --verbosity=2
                        '''
                        echo '✅ Все тесты прошли успешно!'
                    } catch (e) {
                        echo '❌ Некоторые тесты не прошли. Проверьте код.'
                        throw e
                    }
                }
            }
        }

        stage('Collect static') {
            steps {
                bat '''
                    echo "\uD83D\uDCC1 Собираем статические файлы..."
                    python manage.py collectstatic --noinput
                '''
            }
        }

        stage('Deploy Dev') {
            steps {
                bat '''
                    call deploy.bat dev 8001
                '''
            }
        }

        stage('Merge dev -> main (on success)') {
            when {
                expression { return params.MERGE_TO_MAIN }
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: GITHUB_CREDENTIALS_ID, usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_TOKEN')]) {
                        // Подготовка и checkout main
                        bat '''
                            setlocal enableextensions enabledelayedexpansion
                            git config user.name "Jenkins CI"
                            git config user.email "ci@example.local"
                            for /f "delims=" %%i in ('git remote get-url origin') do set ORIGIN_URL=%%i
                            set AUTH_URL=!ORIGIN_URL:https://=https://%GIT_USERNAME%:%GIT_TOKEN%@!
                            git fetch origin +refs/heads/*:refs/remotes/origin/*
                            git checkout -B main origin/main
                        '''

                        // Пытаемся смёрджить dev -> main и читаем код возврата
                        def mergeCode = bat(returnStatus: true, script: '''
                            git merge --no-ff dev -m "Auto-merge dev into main [Jenkins]"
                        ''')

                        if (mergeCode != 0) {
                            echo '⚠️ Конфликт при мердже dev -> main. Требуется ручное разрешение.'
                            bat '''
                                git merge --abort 2>nul || ver >nul
                                git reset --merge 2>nul || ver >nul
                                git checkout -f dev 2>nul || ver >nul
                            '''
                            error 'Merge conflict occurred'
                        }

                        // Пушим main только если merge прошёл успешно
                        bat '''
                            setlocal enableextensions enabledelayedexpansion
                            for /f "delims=" %%i in ('git remote get-url origin') do set ORIGIN_URL=%%i
                            set AUTH_URL=!ORIGIN_URL:https://=https://%GIT_USERNAME%:%GIT_TOKEN%@!
                            git push "!AUTH_URL!" main
                            git checkout dev
                        '''
                    }
                }
            }
        }

        stage('Deploy Prod') {
            steps {
                bat '''
                    rem Обновляем локальный main до origin/main и деплоим
                    git fetch origin +refs/heads/*:refs/remotes/origin/*
                    git checkout -B main origin/main
                    call deploy.bat prod 8000
                    rem Возвращаемся на dev для консистентности
                    git checkout dev
                '''
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


