# YetiAir Flight Booking API

A production-ready FastAPI application for flight booking with SOLID principles, rate limiting, and comprehensive security features.

## ✨ Features

- **SOLID Architecture**: Clean, maintainable code following SOLID principles
- **Rate Limiting**: Protect against abuse with configurable rate limits
- **Security**: Security headers, CORS, error handling
- **Logging**: Comprehensive request/response logging
- **DTOs**: Separation of API contracts and internal data structures
- **Dependency Injection**: Testable, modular services
- **Error Handling**: Centralized exception handling

## 🚀 Quick Start

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env

# 4. Run migrations
python run_migration.py

# 5. Start application
python run.py
```

Visit http://localhost:8000/docs for API documentation.

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Installation and configuration
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and patterns
- **[REFACTORING_GUIDE.md](REFACTORING_GUIDE.md)** - SOLID principles applied
- **[SECURITY_GUIDE.md](SECURITY_GUIDE.md)** - Security features and rate limiting
- **[PROJECT_FLOW.md](PROJECT_FLOW.md)** - Request flow and data flow

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│  API Layer (Handlers)               │
│  - Request validation               │
│  - Rate limiting                    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Facade Layer                       │
│  - Service coordination             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Service Layer                      │
│  - Business logic                   │
│  - Single responsibility            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Infrastructure Layer               │
│  - External APIs                    │
│  - Parsers & Loggers                │
└─────────────────────────────────────┘
```

## 🔒 Security Features

- **Rate Limiting**: Per-endpoint limits (10-50 req/min)
- **Security Headers**: XSS, clickjacking, MIME sniffing protection
- **CORS**: Configurable origin control
- **Error Handling**: No information leakage
- **Request Logging**: Full audit trail

## 📡 API Endpoints

| Endpoint | Method | Rate Limit | Description |
|----------|--------|------------|-------------|
| `/flights/availability` | POST | 20/min | Search flights |
| `/flights/init` | POST | 30/min | Initialize service |
| `/flights/add` | POST | 30/min | Add flight to cart |
| `/flights/booking-session` | POST | 50/min | Get session |
| `/flights/save` | POST | 10/min | Save booking |
| `/flights/itinerary` | POST | 50/min | Get itinerary |

## 🧪 Testing

```bash
# Run tests
pytest src/tests/

# Test rate limiting
for i in {1..25}; do
  curl -X POST http://localhost:8000/flights/availability \
    -H "Content-Type: application/json" \
    -d '{"origin":"KTM","destination":"DEL","depart_date":"20260301","adults":1}'
done
```

## 📁 Project Structure

```
src/
├── main.py                    # Application entry
├── handlers/                  # API endpoints
├── services/                  # Business logic
│   ├── interfaces/           # Service interfaces
│   ├── parsers/              # Response parsers
│   └── loggers/              # Response loggers
├── middleware/               # Middleware components
│   ├── rate_limiter.py      # Rate limiting
│   ├── error_handler.py     # Error handling
│   ├── logging_middleware.py # Request logging
│   └── security_headers.py  # Security headers
├── dtos/                     # Data Transfer Objects
├── schemas/                  # Pydantic schemas
├── models/                   # Database models
├── repositories/             # Data access
└── modules/                  # External clients
```

## 🔧 Configuration

Create `.env` file:

```bash
APP_NAME=YetiAir API
APP_VERSION=1.0.0
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

## 🚢 Production Deployment

### Use Redis for Rate Limiting
```python
# src/middleware/rate_limiter.py
storage_uri="redis://localhost:6379"
```

### Run with Gunicorn
```bash
gunicorn src.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## 🎯 SOLID Principles

- **Single Responsibility**: Each service has one job
- **Open/Closed**: Extend via interfaces, not modification
- **Liskov Substitution**: Interfaces are interchangeable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions

## 📊 Monitoring

```bash
# Health check
curl http://localhost:8000/liveness

# View logs
tail -f logs/app.log

# Monitor rate limits
grep "Rate limit exceeded" logs/app.log
```

## 🤝 Contributing

1. Follow SOLID principles
2. Add tests for new features
3. Update documentation
4. Ensure rate limits are appropriate

## 📝 License

MIT License

## 🔗 Links

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
