@echo off
echo ============================================
echo  Smart Parking System - Setup Script
echo ============================================
echo.

REM Check Python version
python --version 2>NUL
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+ and add to PATH.
    pause
    exit /b
)

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo Step 3: Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements.
    pause
    exit /b
)

echo Step 4: Running database migrations...
python manage.py migrate

echo Step 5: Seeding database with demo data and AI training...
python manage.py seed_data

echo.
echo ============================================
echo  SETUP COMPLETE!
echo ============================================
echo.
echo  Admin Login : username=admin  password=admin123
echo  User  Login : username=demo   password=demo1234
echo.
echo  Starting server...
echo  Open browser at: http://127.0.0.1:8000
echo.
python manage.py runserver
pause
