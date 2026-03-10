#!/bin/bash

set -e

echo "========================================="
echo "Stock Market Platform - Quick Start"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "Creating .env file..."
    cat > backend/.env << EOF
APP_NAME=Stock Market Platform
DEBUG=true
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/stock_market
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-change-in-production
ALPHA_VANTAGE_API_KEY=
FINNHUB_API_KEY=
OPENAI_API_KEY=
EOF
    echo "✓ Created backend/.env file"
fi

# Stop any running containers
echo ""
echo "Stopping any running containers..."
docker-compose down 2>/dev/null || true

# Build and start services
echo ""
echo "Building and starting services..."
echo "This may take a few minutes on first run..."
docker-compose up -d --build

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo ""
echo "Checking service status..."
docker-compose ps

# Initialize database
echo ""
echo "Initializing database..."
docker-compose exec -T backend python -c "
from app.core.database import engine, Base
from app.models import models
Base.metadata.create_all(bind=engine)
print('Database tables created successfully!')
" 2>/dev/null || echo "⚠️  Database initialization skipped or failed"

echo ""
echo "========================================="
echo "✓ Stock Market Platform is running!"
echo "========================================="
echo ""
echo "Access the application:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop the application:"
echo "  docker-compose down"
echo ""
