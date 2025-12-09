@echo off
REM BookClub Platform Setup Script for Windows

echo ================================
echo BookClub Platform - Setup Script
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is required but not installed.
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is required but not installed.
    exit /b 1
)

echo [OK] Prerequisites check passed
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Copy .env if not exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo WARNING: Please edit backend\.env with your credentials
)

cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...
cd frontend

REM Check if frontend exists
if exist "package.json" (
    echo Installing Node dependencies...
    call npm install

    REM Copy .env if not exists
    if not exist ".env" (
        echo Creating .env file from template...
        copy .env.example .env
        echo WARNING: Please edit frontend\.env with your credentials
    )
) else (
    echo WARNING: Frontend directory not ready yet. Run 'npm install' in frontend\ when ready.
)

cd ..

REM Setup Database
echo.
echo Setting up Database...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Starting PostgreSQL with Docker...
    docker run -d --name bookclub-db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bookclub -p 5432:5432 postgres:15
    echo Waiting for database to be ready...
    timeout /t 3 /nobreak >nul
) else (
    echo WARNING: Docker not found. Please install and start PostgreSQL manually
)

echo.
echo ================================
echo Setup complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit backend\.env with your Google OAuth credentials
echo 2. Edit frontend\.env with your API URL and Google Client ID
echo 3. Generate a SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
echo 4. Run migrations: cd backend ^&^& venv\Scripts\activate ^&^& alembic upgrade head
echo 5. Start backend: cd backend ^&^& uvicorn app.main:app --reload
echo 6. Start frontend: cd frontend ^&^& npm run dev
echo.
echo See QUICKSTART.md for detailed instructions
echo.
pause
