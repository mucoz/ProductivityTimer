@echo off
title Productivity Timer - Launcher
color 0A

echo ========================================
echo    Productivity Timer Launcher
echo ========================================
echo.

REM Python check
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Python version check
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python version: %PYTHON_VERSION%

REM Virtual environment check
if not exist "venv\" (
    echo.
    echo [INFO] Virtual environment not found, creating...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
) else (
    echo [OK] Virtual environment exists.
)

REM Activate virtual environment
echo.
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated.

REM Requirements check
echo.
echo [INFO] Checking requirements...

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found!
    echo [INFO] Creating requirements.txt...
    echo screeninfo>> requirements.txt
    echo.
)

REM Check installed packages
pip list --format=freeze > installed_temp.txt

set NEED_INSTALL=0
for /f "delims== tokens=1" %%i in (requirements.txt) do (
    findstr /i /c:"%%i" installed_temp.txt >nul
    if %errorlevel% neq 0 (
        set NEED_INSTALL=1
    )
)
del installed_temp.txt

if %NEED_INSTALL% equ 1 (
    echo [INFO] Missing packages found, installing...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install packages!
        pause
        exit /b 1
    )
    echo [OK] All packages installed successfully.
) else (
    echo [OK] All requirements satisfied.
)

REM Run main program
echo.
echo ========================================
echo    Starting program...
echo ========================================
echo.

python main.py

REM When program closes
echo.
echo ========================================
echo    Program terminated.
echo ========================================
echo.

REM Deactivate virtual environment
call deactivate

pause