@echo off
REM AI Training Assistant Startup Script for Windows

echo.
echo ============================================
echo   AI Training Assistant Startup
echo ============================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [OK] Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r backend\requirements.txt >nul 2>&1
echo [OK] Backend dependencies installed

pip install -r frontend\requirements.txt >nul 2>&1
echo [OK] Frontend dependencies installed

REM Create database directory
if not exist "database\sqlite" (
    mkdir database\sqlite
)

REM Check if database exists
if not exist "database\sqlite\training_assistant.db" (
    echo [INFO] Creating database...
    sqlite3 database\sqlite\training_assistant.db < database\schema.sql
    echo [OK] Database created
)

REM Check if .env exists
if not exist ".env" (
    echo [INFO] Creating .env file...
    if exist ".env.example" (
        copy .env.example .env
    ) else (
        (echo GROQ_API_KEY=your_api_key_here) > .env
    )
    echo [WARNING] Please set your GROQ_API_KEY in .env file
)

echo.
echo ============================================
echo   Ready to start!
echo ============================================
echo.
echo Option 1: Start Backend Server
echo Command: cd backend ^& uvicorn main:app --reload
echo.
echo Option 2: Start Frontend
echo Command: cd frontend ^& streamlit run main.py
echo.
echo Option 3: Start Both (in separate terminals)
echo.
pause
