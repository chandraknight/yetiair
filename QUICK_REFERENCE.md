# Quick Reference Guide

## 🚀 Common Commands

```bash
# Start application
python run.py

# Install dependencies
pip install -r requirements.txt

# Run migrations
python run_migration.py

# View logs
tail -f logs/app.log

# Health check
curl http://localhost:8000/liveness
```

## 📡 API Endpoints Quick Reference

```bash
# Initialize service
curl -X POST http://localhost:8000/flights/init

# Search flights
curl -X POST http://localhost:8000/flights/availability \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "KTM",
    "destination": "DEL",
    "depart_date": "20260301",
    "adults": 1
  }'

# Add flight
curl -X POST http://localhost:8000/flights/add \
  -H "Content-Type: application/json" \
  -d '{
    "search_id": "your-search-id",
    "flight_id": "flight-123",
    "origin": "KTM",
    "destination": "DEL",
    "adults": 1
  }'
```

## 🔒 Rate Limits

| Endpoint | Limit | Use Case |
|----------|-------|----------|
| `/flights/availability` | 20/min | Search flights |
| `/flights/init` | 30/min | Initialize |
| `/flights/add` | 30/min | Add to cart |
| `/flights/booking-session` | 50/min | Get session |
| `/flights/save` | 10/min | Book flight |
| `/flights/itinerary` | 50/min | Get details |

## 🏗️ Architecture Layers

```
Handler → Facade → Service → Infrastructure
  ↓         ↓         ↓           ↓
Schema    DTO      DTO      External API
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/main.py` | App initialization |
| `src/handlers/flight_handler.py` | API endpoints |
| `src/services/flight_service_facade.py` | Service coordinator |
| `src/middleware/rate_limiter.py` | Rate limiting |
| `src/middleware/error_handler.py` | Error handling |

## 🔧 Configuration

```bash
# .env file
APP_NAME=YetiAir API
DATABASE_URL=postgresql+asyncpg://...
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

## 🧪 Testing Rate Limits

```bash
# Test availability endpoint (20/min limit)
for i in {1..25}; do
  curl -X POST http://localhost:8000/flights/availability \
    -H "Content-Type: application/json" \
    -d '{"origin":"KTM","destination":"DEL","depart_date":"20260301","adults":1}'
  echo "Request $i"
done
```

## 🎯 SOLID Principles Applied

- **S**ingle Responsibility: Each service has one job
- **O**pen/Closed: Extend via interfaces
- **L**iskov Substitution: Interfaces are interchangeable
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions

## 🔍 Debugging

```bash
# Check logs
tail -f logs/app.log

# Check specific search
tail -f logs/search_*.log

# Check rate limit hits
grep "Rate limit exceeded" logs/app.log

# Check errors
grep "ERROR" logs/app.log
```

## 📊 Monitoring

```bash
# Health check
curl http://localhost:8000/liveness

# API docs
open http://localhost:8000/docs

# Check response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/liveness
```

## 🚢 Production Checklist

- [ ] Update rate limiter to use Redis
- [ ] Configure ALLOWED_ORIGINS
- [ ] Setup HTTPS/SSL
- [ ] Configure log rotation
- [ ] Setup monitoring/alerting
- [ ] Run with gunicorn
- [ ] Setup reverse proxy (nginx)
- [ ] Configure firewall
- [ ] Setup backup strategy
- [ ] Document runbook

## 📚 Documentation Index

1. **[README.md](README.md)** - Project overview
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
4. **[REFACTORING_GUIDE.md](REFACTORING_GUIDE.md)** - SOLID principles
5. **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** - Security features
6. **[PROJECT_FLOW.md](PROJECT_FLOW.md)** - Request flow
7. **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - What changed
8. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - This file

## 🆘 Common Issues

### Rate Limit Not Working
```bash
pip install slowapi
```

### CORS Errors
```bash
# Update .env
ALLOWED_ORIGINS=http://localhost:3000
```

### Import Errors
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Database Connection Failed
```bash
# Check DATABASE_URL in .env
psql $DATABASE_URL
```

## 💡 Tips

- Use `/docs` for interactive API testing
- Check logs for detailed error messages
- Rate limits are per IP address
- Use Redis in production for rate limiting
- Monitor rate limit hits for abuse detection
- Keep security headers enabled
- Regular log rotation recommended

## 🔗 Useful Links

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/liveness
