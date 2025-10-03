@echo off
setlocal enabledelayedexpansion

:: Usage: deploy.bat dev 8001  or deploy.bat prod 8000
set ENV=%1
set PORT=%2

if "%ENV%"=="" (
  echo Usage: deploy.bat ^<dev|prod^> ^<port^>
  exit /b 1
)

if "%PORT%"=="" (
  echo Usage: deploy.bat ^<dev|prod^> ^<port^>
  exit /b 1
)

echo ===============================
echo Deploy to %ENV% on port %PORT%
echo ===============================

echo Stopping process on port %PORT% (if any)...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT%" ^| findstr LISTENING') do (
  echo Killing PID %%p
  taskkill /F /PID %%p >nul 2>&1
)

echo Applying migrations...
python manage.py migrate --noinput

REM Добавлено: сборка статики для корректной работы collectstatic в CI
python manage.py collectstatic --noinput

echo Starting server in background...
:: Start in a new window minimized; logs to deploy_%ENV%.log
start "django-%ENV%" /MIN cmd /c "python manage.py runserver 0.0.0.0:%PORT% 1>>deploy_%ENV%.log 2>&1"

echo ✅ Deploy completed: %ENV% on http://localhost:%PORT%
exit /b 0


