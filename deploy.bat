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

echo Starting server in background...
:: Start in a new window minimized; logs to deploy_%ENV%.log
start "django-%ENV%" /MIN cmd /c "python manage.py runserver 0.0.0.0:%PORT% 1>>deploy_%ENV%.log 2>&1"

echo ✅ Deploy completed: %ENV% on http://localhost:%PORT%
exit /b 0

@echo off
setlocal enableextensions enabledelayedexpansion

REM Usage: deploy.bat dev|prod
set ENV=%1
if "%ENV%"=="" (
  echo Usage: deploy.bat dev^|prod
  exit /b 1
)

if /I "%ENV%"=="dev"  set PORT=8001
if /I "%ENV%"=="prod" set PORT=8000

if "%PORT%"=="" (
  echo Unknown environment: %ENV%
  exit /b 1
)

echo ==================================================
echo Deploying %ENV% environment on port %PORT%
echo Workspace: %CD%
echo ==================================================

REM Apply migrations before start (safe to run multiple times)
call python manage.py makemigrations --noinput
if errorlevel 1 echo Warning: makemigrations returned non-zero
call python manage.py migrate --noinput
if errorlevel 1 (
  echo ERROR: migrate failed
  exit /b 1
)

REM Start server in background window to not block Jenkins
echo Starting Django server on 0.0.0.0:%PORT% ...
start "django-%ENV%" cmd /c "python manage.py runserver 0.0.0.0:%PORT%"

echo ✅ Deploy %ENV% initiated. Server should come up shortly on http://localhost:%PORT%
exit /b 0


