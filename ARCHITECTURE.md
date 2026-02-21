# Flight Service Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Flight Handler                          │
│                  (FastAPI Endpoints)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              FlightServiceFacade                            │
│         (Unified Interface - Facade Pattern)                │
└─┬───────────┬──────────┬──────────┬────────────────────────┘
  │           │          │          │
  ▼           ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────────┐
│Flight│  │Flight│  │Book- │  │Service   │
│Avail │  │Add   │  │ing   │  │Init      │
│Svc   │  │Svc   │  │Svc   │  │Svc       │
└──┬───┘  └──┬───┘  └──┬───┘  └────┬─────┘
   │         │         │            │
   │ ┌───────┴─────────┘            │
   │ │                              │
   ▼ ▼                              ▼
┌─────────────────┐         ┌──────────────┐
│  IResponseParser│         │ Yeti Client  │
│  IResponseLogger│         │              │
└────┬────────────┘         └──────────────┘
     │
     ▼
┌─────────────────────────────┐
│  XmlResponseParser          │
│  FileResponseLogger         │
└─────────────────────────────┘
```

## Data Flow

```
Request (Schema) → Handler → Facade → Service → DTO → External API
                                         ↓
                                      Parser
                                         ↓
                                      Logger
                                         ↓
Response (Schema) ← Handler ← Facade ← DTO
```

## Layer Responsibilities

### 1. Handler Layer
- Receives HTTP requests
- Validates input (Pydantic schemas)
- Calls facade
- Returns HTTP responses
- Handles exceptions

### 2. Facade Layer
- Provides unified interface
- Coordinates between services
- Converts DTOs to schemas
- Manages service dependencies

### 3. Service Layer
- Implements business logic
- Single responsibility per service
- Uses dependency injection
- Returns DTOs

### 4. Infrastructure Layer
- Parsers: Transform external data
- Loggers: Persist responses
- Clients: Communicate with external APIs

## Key Design Patterns

### 1. Facade Pattern
`FlightServiceFacade` provides a simplified interface to complex subsystems

### 2. Dependency Injection
Services receive dependencies through constructors:
```python
def __init__(self, parser: IResponseParser, logger: IResponseLogger)
```

### 3. Strategy Pattern
Different parsers/loggers can be swapped via interfaces

### 4. DTO Pattern
Internal data transfer separated from API contracts

## Extension Points

### Adding a New Parser
```python
class JsonResponseParser(IResponseParser):
    def parse(self, raw_response: str) -> Dict[str, Any]:
        return json.loads(raw_response)
```

### Adding a New Logger
```python
class DatabaseResponseLogger(IResponseLogger):
    def log_response(self, search_id: str, filename: str, content: Any):
        # Save to database
        pass
```

### Adding a New Service
```python
class PriceCalculationService:
    def __init__(self, parser: IResponseParser):
        self._parser = parser
    
    async def calculate_price(self, request: PriceRequest) -> PriceDTO:
        # Implementation
        pass
```

## Testing Strategy

### Unit Tests
- Mock interfaces for isolated testing
- Test each service independently
- Verify parser/logger behavior

### Integration Tests
- Test facade with real implementations
- Verify service coordination
- Test end-to-end flows

### Example
```python
def test_flight_availability_service():
    # Arrange
    mock_parser = Mock(spec=IResponseParser)
    mock_logger = Mock(spec=IResponseLogger)
    mock_parser.parse.return_value = {"flights": []}
    
    service = FlightAvailabilityService(mock_parser, mock_logger)
    
    # Act
    result = await service.check_availability(request, "search-123")
    
    # Assert
    assert result.search_id == "search-123"
    mock_parser.parse.assert_called_once()
    mock_logger.log_response.assert_called_once()
```
