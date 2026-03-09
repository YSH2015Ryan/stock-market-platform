# Deployment Guide

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone <repository-url>
cd stock-market-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and configure:
- Database credentials
- API keys (Alpha Vantage, OpenAI, etc.)
- Application secrets

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Backend API (port 8000)
- Frontend web app (port 3000)
- Data crawler (background service)

### 4. Verify Services

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f crawler
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Manual Deployment

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:pass@localhost:5432/stock_market"
export REDIS_URL="redis://localhost:6379/0"
export OPENAI_API_KEY="your_key"

# Initialize database
# Tables are created automatically by SQLAlchemy
# Or run migrations if using Alembic:
# alembic upgrade head

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev

# Or build for production
npm run build
npm start
```

### Crawler Setup

```bash
cd crawler

# Install dependencies
pip install -r requirements.txt

# Start scheduler
python scheduler.py
```

## Production Deployment

### Using Docker Compose (Production)

```bash
# Build production images
docker-compose -f docker-compose.yml build

# Start with production profile
docker-compose --profile production up -d
```

### Environment Variables (Production)

**Critical settings to change:**

```env
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-strong-random-key>

# Use strong database password
DATABASE_PASSWORD=<strong-password>

# Configure CORS for your domain
CORS_ORIGINS=https://yourdomain.com

# Configure allowed hosts
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres stock_market > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres stock_market < backup.sql
```

### Monitoring

```bash
# View resource usage
docker stats

# Check logs for errors
docker-compose logs --tail=100 -f

# Backend health check
curl http://localhost:8000/health
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Connect to database manually
docker-compose exec postgres psql -U postgres -d stock_market
```

### API Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Restart backend service
docker-compose restart backend

# Check if port is in use
netstat -an | grep 8000
```

### Frontend Build Errors

```bash
# Clear Next.js cache
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Crawler Issues

```bash
# Check crawler logs
docker-compose logs crawler

# Restart crawler
docker-compose restart crawler

# Test crawler manually
docker-compose exec crawler python -c "from scheduler import CrawlerScheduler; s = CrawlerScheduler(); s.update_market_data()"
```

## Scaling

### Horizontal Scaling

To scale backend API:

```bash
docker-compose up -d --scale backend=3
```

Add a load balancer (nginx) configuration.

### Database Optimization

- Add read replicas for PostgreSQL
- Configure connection pooling
- Enable query caching in Redis

### Caching Strategy

- Use Redis for API response caching
- Cache market data for 5 minutes
- Cache reports for 1 hour

## Security Checklist

- [ ] Change all default passwords
- [ ] Configure firewall rules
- [ ] Enable HTTPS with SSL certificates
- [ ] Set up regular database backups
- [ ] Configure rate limiting
- [ ] Enable security headers
- [ ] Implement API authentication
- [ ] Regular security updates

## Maintenance

### Regular Tasks

- Weekly database backups
- Monthly dependency updates
- Log rotation and cleanup
- Performance monitoring
- Security patches

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose down
docker-compose build
docker-compose up -d

# Check for database migrations
# If using Alembic:
docker-compose exec backend alembic upgrade head
```

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review documentation
- Submit GitHub issues
- Contact support team
