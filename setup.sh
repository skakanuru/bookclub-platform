#!/bin/bash

# BookClub Platform Setup Script

echo "🚀 BookClub Platform - Setup Script"
echo "===================================="
echo ""

# Check if required commands exist
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "⚠️  Docker not found. You'll need to install PostgreSQL manually." >&2; }

echo "✅ Prerequisites check passed"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your credentials"
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Check if frontend exists (it might still be building)
if [ -f "package.json" ]; then
    echo "Installing Node dependencies..."
    npm install

    # Copy .env if not exists
    if [ ! -f ".env" ]; then
        echo "Creating .env file from template..."
        cp .env.example .env
        echo "⚠️  Please edit frontend/.env with your credentials"
    fi
else
    echo "⚠️  Frontend directory not ready yet. Run 'npm install' in frontend/ when ready."
fi

cd ..

# Setup Database
echo ""
echo "🗄️  Setting up Database..."
if command -v docker >/dev/null 2>&1; then
    echo "Starting PostgreSQL with Docker..."
    docker run -d \
        --name bookclub-db \
        -e POSTGRES_PASSWORD=password \
        -e POSTGRES_DB=bookclub \
        -p 5432:5432 \
        postgres:15 || echo "⚠️  Database container already exists or failed to start"

    echo "Waiting for database to be ready..."
    sleep 3
else
    echo "⚠️  Please install and start PostgreSQL manually"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your Google OAuth credentials"
echo "2. Edit frontend/.env with your API URL and Google Client ID"
echo "3. Generate a SECRET_KEY: python -c 'import secrets; print(secrets.token_hex(32))'"
echo "4. Run migrations: cd backend && source venv/bin/activate && alembic upgrade head"
echo "5. Start backend: cd backend && uvicorn app.main:app --reload"
echo "6. Start frontend: cd frontend && npm run dev"
echo ""
echo "📖 See QUICKSTART.md for detailed instructions"
