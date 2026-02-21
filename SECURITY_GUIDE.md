# Security & Rate Limiting Guide

## Overview
The application now includes comprehensive security features and rate limiting to protect against abuse and common vulnerabilities.

## Rate Limiting

### Implementation
Rate limiting is implemented using `slowapi` with in-memory storage. Each endpoint has specific limits based on its criticality.

### Rate Limits by Endpoint

| Endpoint | Limit | Reason |
|----------|-------|--------|
| `/flights/availability` | 20/minute | Search operations are resource-intensive |
| `/flights/init` | 30/minute | Service initialization |
| `/flights/add` | 30/minute | Adding flights to cart |
| `/flights/booking-session` | 50/minute | Session retrieval is lightweight |
| `/flights/save` | 10/minute | Critical operation - booking creation |
| `/flights/itinerary` | 50/minute | Read-only operation |
| Global default | 100/minute | Applies to all other endpoints |

### Rate Limit Response
When rate limit is exceeded, the API returns:
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later.",
  "detail": "20 per 1 minute"
}
```
Status Code: `429 Too Many Requests`

### Customizing Rate Limits
To change rate limits, edit the decorator in `src/handlers/flight_handler.py`:
```python
@limiter.limit("50/minute")  # Change this value
async def endpoint_name(...):
    ...
```

### Production Considerations
For production, consider using Redis for distributed rate limiting:
```python
# In src/middleware/rate_limiter.py
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    storage_uri="redis://localhost:6379",  # Use Redis
    strategy="fixed-window"
)
```

## Security Features

### 1. Security Headers
All responses include security headers:
- `X-Content-Type-Options: nosniff` - Prevents MIME sniffing
- `X-Frame-Options: DENY` - Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` - XSS protection
- `Strict-Transport-Security` - Forces HTTPS
- `Content-Security-Policy` - Restricts resource loading

### 2. CORS Configuration
CORS is configured to control which origins can access the API.

To customize allowed origins, update `src/config.py`:
```python
ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

### 3. Error Handling
Centralized error handling prevents information leakage:
- Custom exceptions return structured error responses
- Generic exceptions return safe error messages
- Stack traces are logged but not exposed to clients

### 4. Request/Response Logging
All requests and responses are logged with:
- HTTP method and path
- Client IP address
- Response status code
- Request duration
- Timestamp

## Middleware Stack

Middleware is applied in this order (outermost to innermost):
1. **SecurityHeadersMiddleware** - Adds security headers
2. **LoggingMiddleware** - Logs requests/responses
3. **CORSMiddleware** - Handles CORS
4. **Rate Limiter** - Enforces rate limits
5. **Error Handlers** - Catches and formats errors

## Exception Hierarchy

```
Exception
├── BaseAppException (legacy)
└── BaseCustomException
    ├── ValidationException (422)
    ├── RateLimitException (429)
    └── ServiceUnavailableException (503)
```

### Using Custom Exceptions
```python
from src.exceptions.validation_exception import ValidationException

if not valid_data:
    raise ValidationException(
        message="Invalid flight data",
        details={"field": "origin", "error": "Required"}
    )
```

## Best Practices

### 1. Rate Limiting Strategy
- **Search endpoints**: Lower limits (resource-intensive)
- **Booking endpoints**: Very low limits (critical operations)
- **Read endpoints**: Higher limits (less risky)

### 2. Monitoring
Monitor these metrics:
- Rate limit hits per endpoint
- Error rates by type
- Response times
- Failed authentication attempts

### 3. IP-based Limiting
Current implementation uses client IP. Consider:
- Using API keys for authenticated users
- Different limits for authenticated vs anonymous
- Whitelist trusted IPs

### 4. Graceful Degradation
When rate limited:
- Return clear error messages
- Include retry-after information
- Log for monitoring

## Configuration

### Environment Variables
Add to `.env`:
```bash
# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_STORAGE=memory://
# For production: redis://localhost:6379

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Security
ENABLE_SECURITY_HEADERS=true
```

## Testing Rate Limits

### Manual Testing
```bash
# Test rate limit
for i in {1..25}; do
  curl -X POST http://localhost:8000/flights/availability \
    -H "Content-Type: application/json" \
    -d '{"origin":"KTM","destination":"DEL","depart_date":"20260301","adults":1}'
  echo "Request $i"
done
```

### Expected Behavior
- First 20 requests: Success (200)
- Requests 21+: Rate limited (429)

## Upgrading to Redis

1. Install Redis:
```bash
pip install redis
```

2. Update rate limiter:
```python
storage_uri="redis://localhost:6379"
```

3. Benefits:
- Distributed rate limiting across multiple servers
- Persistent rate limit counters
- Better performance at scale

## Security Checklist

- [x] Rate limiting enabled
- [x] Security headers configured
- [x] CORS properly configured
- [x] Error handling doesn't leak information
- [x] Request/response logging
- [ ] HTTPS enforced (configure in deployment)
- [ ] API authentication (implement as needed)
- [ ] Input validation (Pydantic schemas)
- [ ] SQL injection protection (SQLAlchemy ORM)
- [ ] Redis for production rate limiting
