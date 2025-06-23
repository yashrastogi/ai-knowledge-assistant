#!/bin/bash

# Setup script for AI Knowledge Assistant
# This script sets up both backend and frontend environments

set -e

echo "🚀 Setting up AI Knowledge Assistant..."

# Backend setup
echo ""
echo "📦 Setting up Backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
echo "Installing Node dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your OPENAI_API_KEY"
echo "2. Start backend: cd backend && source venv/bin/activate && python main.py"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "Backend will run on: http://localhost:8000"
echo "Frontend will run on: http://localhost:5173"
echo ""
