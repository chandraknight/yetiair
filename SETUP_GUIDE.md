# Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Database Migrations
```bash
python run_migration.py
```

### 4. Start the Application
```bash
python run.py
```

### 5. Verify Installation
```bash
curl http://localhost:8000/liveness
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-02-21T..."
}
```

## Testing Rate Limiting

### Test Flight Availability Rate Limit (20/min)
```bash
# This script will hit the rate limit
for i in {1..25}; do
  curl -X POST http://localhost:8000/flights/availability \
    -H "Content-Type: application/json" \
    -d '{
      "origin": "KTM",
      "destination": "DEL",
      "depart_date": "20260301",
      "adults": 1
    }'
  echo "\nRequest $i completed"
  sleep 1
done
```

Expected:
- Requests 1-20: Success (200)
- Requests 21+: Rate limited (429)

## Project Structure

```
.
├── src/
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Configuration
│   ├── handlers/                  # API endpoints
│   │   ├── flight_handler.py     # Flight endpoints
│   │   └── liveness_handler.py   # Health check
│   ├── services/                  # Business logic
│   │   ├── flight_service_facade.py
│   │   ├── flight_availability_service.py
│   │   ├── flight_add_service.py
│   │   ├── booking_service.py
│   │   ├── interfaces/           # Service interfaces
│   │   ├── parsers/              # Response parsers
│   │   └── loggers/              # Response loggers
│   ├── middleware/               # Middleware components
│   │   ├── rate_limiter.py      # Rate limiting
│   │   ├── error_handler.py     # Error handling
│   │   ├── logging_middleware.py # Request logging
│   │   ├── security_headers.py  # Security headers
│   │   └── cors_middleware.py   # CORS config
│   ├── dtos/                     # Data Transfer Objects
│   ├── schemas/                  # Pydantic schemas
│   ├── models/                   # Database models
│   ├── repositories/             # Data access
│   ├── modules/                  # External clients
│   ├── exceptions/               # Custom exceptions
│   └── utils/                    # Utilities
├── logs/                         # Application logs
├── requirements.txt              # Dependencies
├── run.py                        # Run script
└── .env                          # Environment config
```

## Configuration

### Environment Variables (.env)

```bash
# Application
APP_NAME=YetiAir API
APP_VERSION=1.0.0

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname

# Redis (optional, for rate limiting)
REDIS_URL=redis://localhost:6379

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Logging
LOG_LEVEL=INFO
```

## Development

### Running in Development Mode
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
pytest src/tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/
```

## Production Deployment

### 1. Update Rate Limiter for Redis
Edit `src/middleware/rate_limiter.py`:
```python
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri="redis://localhost:6379",  # Use Redis
    strategy="fixed-window"
)
```

### 2. Install Redis
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

### 3. Use Production Server
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### 4. Setup Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 5. Setup SSL with Let's Encrypt
```bash
sudo certbot --nginx -d yourdomain.com
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/liveness
```

### View Logs
```bash
# Application logs
tail -f logs/app.log

# Search logs
tail -f logs/search_*.log
```

### Monitor Rate Limits
Check logs for rate limit hits:
```bash
grep "Rate limit exceeded" logs/app.log
```

## Troubleshooting

### Issue: Rate Limiter Not Working
**Solution**: Ensure slowapi is installed
```bash
pip install slowapi
```

### Issue: CORS Errors
**Solution**: Update ALLOWED_ORIGINS in .env
```bash
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Issue: Database Connection Failed
**Solution**: Check DATABASE_URL and ensure database is running
```bash
# Test connection
psql $DATABASE_URL
```

### Issue: Import Errors
**Solution**: Ensure you're in the project root and PYTHONPATH is set
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

1. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Review [REFACTORING_GUIDE.md](REFACTORING_GUIDE.md) for SOLID principles
3. Review [SECURITY_GUIDE.md](SECURITY_GUIDE.md) for security features
4. Review [PROJECT_FLOW.md](PROJECT_FLOW.md) for request flow
