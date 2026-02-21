# Project Flow Documentation

## Application Startup Flow

```
1. run.py
   ↓
2. src/main.py → create_app()
   ↓
3. Initialize FastAPI app
   ↓
4. Setup Rate Limiter (slowapi)
   ↓
5. Register Exception Handlers
   ↓
6. Add Middleware Stack:
   - SecurityHeadersMiddleware
   - LoggingMiddleware
   - CORSMiddleware
   ↓
7. Include Routers:
   - /liveness (health checks)
   - /flights (flight operations)
   ↓
8. Startup Event → Log initialization
   ↓
9. Application Ready
```

## Request Flow

```
Client Request
   ↓
[SecurityHeadersMiddleware] → Add security headers
   ↓
[LoggingMiddleware] → Log request details
   ↓
[CORSMiddleware] → Validate origin
   ↓
[Rate Limiter] → Check rate limit
   ↓
[Router] → Match endpoint
   ↓
[Handler] → Validate request (Pydantic)
   ↓
[Facade] → Coordinate services
   ↓
[Service] → Business logic
   ↓
[Parser] → Parse external response
   ↓
[Logger] → Log response
   ↓
[DTO] → Internal data transfer
   ↓
[Schema] → Convert to API response
   ↓
[Handler] → Return response
   ↓
[Middleware] → Add headers, log response
   ↓
Client Response
```

## Flight Availability Flow

```
POST /flights/availability
   ↓
1. Rate Limit Check (20/min)
   ↓
2. Generate search_id (UUID)
   ↓
3. Validate FlightAvailabilityRequest
   ↓
4. FlightServiceFacade.check_availability()
   ↓
5. FlightAvailabilityService.check_availability()
   ↓
6. YetiClient.get_flight_availability()
   ↓
7. External API Call (XML)
   ↓
8. XmlResponseParser.parse()
   ↓
9. Create ServiceResponseDTO
   ↓
10. FileResponseLogger.log_response()
   ↓
11. Convert DTO → FlightAvailabilityResponse
   ↓
12. Return JSON response
```

## Booking Flow

```
1. POST /flights/init
   ↓ Initialize session
   
2. POST /flights/availability
   ↓ Search flights
   
3. POST /flights/add
   ↓ Add flight to cart
   
4. POST /flights/booking-session
   ↓ Get session details
   
5. POST /flights/save
   ↓ Save booking (10/min limit)
   
6. POST /flights/itinerary
   ↓ Get confirmation
```

## Service Layer Architecture

```
FlightServiceFacade (Coordinator)
   ├── FlightAvailabilityService
   │   ├── YetiClient
   │   ├── XmlResponseParser
   │   └── FileResponseLogger
   │
   ├── FlightAddService
   │   ├── YetiClient
   │   ├── XmlResponseParser
   │   └── FileResponseLogger
   │
   ├── BookingService
   │   └── YetiClient
   │
   └── ServiceInitializationService
       └── YetiClient
```

## Data Flow Layers

```
┌─────────────────────────────────────┐
│  API Layer (Pydantic Schemas)      │
│  - Request validation               │
│  - Response serialization           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Handler Layer                      │
│  - Route handling                   │
│  - Error handling                   │
│  - Logging                          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Facade Layer                       │
│  - Service coordination             │
│  - DTO ↔ Schema conversion         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Service Layer (DTOs)               │
│  - Business logic                   │
│  - Single responsibility            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Infrastructure Layer               │
│  - External API clients             │
│  - Parsers                          │
│  - Loggers                          │
└─────────────────────────────────────┘
```

## Error Handling Flow

```
Exception Raised
   ↓
Is BaseCustomException?
   ├─ Yes → custom_exception_handler
   │         ↓
   │         Return structured error
   │         {error, message, details}
   │
   └─ No → general_exception_handler
             ↓
             Log full error
             ↓
             Return safe error message
             (no stack trace to client)
```

## Rate Limiting Flow

```
Request Received
   ↓
Extract Client IP
   ↓
Check Rate Limit Storage
   ↓
Limit Exceeded?
   ├─ Yes → Return 429
   │         {error, message, detail}
   │
   └─ No → Increment Counter
             ↓
             Process Request
```

## Logging Flow

```
Request Arrives
   ↓
[LoggingMiddleware]
   ↓
Log: Method, Path, Client IP
   ↓
Start Timer
   ↓
Process Request
   ↓
Calculate Duration
   ↓
Log: Status Code, Duration
   ↓
[Handler Level]
   ↓
Log: Business events
   ↓
[Service Level]
   ↓
Log: External API calls
   ↓
[FileResponseLogger]
   ↓
Save: JSON responses to files
```

## Configuration Flow

```
.env file
   ↓
python-dotenv loads
   ↓
src/config.py (Settings)
   ↓
Pydantic validation
   ↓
Available as settings object
   ↓
Used by:
   - main.py (app config)
   - db.py (database)
   - clients (external APIs)
```

## Dependency Injection Flow

```
FlightServiceFacade.__init__()
   ↓
Create Parser: XmlResponseParser()
   ↓
Create Logger: FileResponseLogger()
   ↓
Inject into Services:
   - FlightAvailabilityService(parser, logger)
   - FlightAddService(parser, logger)
   ↓
Services use interfaces:
   - IResponseParser
   - IResponseLogger
   ↓
Easy to swap implementations
```

## Testing Flow

```
Unit Tests
   ├── Mock IResponseParser
   ├── Mock IResponseLogger
   ├── Mock YetiClient
   └── Test Service Logic
   
Integration Tests
   ├── Test Facade coordination
   ├── Test Handler → Service flow
   └── Test with real parsers/loggers
   
E2E Tests
   ├── Test full request flow
   ├── Test rate limiting
   └── Test error handling
```

## Deployment Flow

```
1. Install dependencies
   pip install -r requirements.txt
   
2. Setup environment
   cp .env.example .env
   
3. Run migrations
   python run_migration.py
   
4. Start application
   python run.py
   
5. Health check
   GET /liveness
   
6. Monitor logs
   tail -f logs/*.log
```

## Key Files & Responsibilities

| File | Responsibility |
|------|----------------|
| `src/main.py` | App initialization, middleware setup |
| `src/handlers/flight_handler.py` | API endpoints, request validation |
| `src/services/flight_service_facade.py` | Service coordination |
| `src/services/*_service.py` | Business logic |
| `src/middleware/rate_limiter.py` | Rate limiting |
| `src/middleware/error_handler.py` | Error handling |
| `src/middleware/logging_middleware.py` | Request/response logging |
| `src/middleware/security_headers.py` | Security headers |
| `src/dtos/*.py` | Internal data transfer |
| `src/schemas/*.py` | API contracts |
| `src/modules/yeti_client.py` | External API client |

## Performance Considerations

1. **Rate Limiting**: In-memory (dev) → Redis (prod)
2. **Logging**: Async logging for better performance
3. **Parsing**: Cached parsers, reusable instances
4. **Database**: Connection pooling via SQLAlchemy
5. **External APIs**: Timeout configuration, retry logic

## Security Layers

```
1. Rate Limiting → Prevent abuse
2. Input Validation → Pydantic schemas
3. CORS → Control origins
4. Security Headers → Browser protection
5. Error Handling → No information leakage
6. Logging → Audit trail
7. HTTPS → Transport security (production)
```
