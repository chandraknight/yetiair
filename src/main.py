from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from src.config import settings
from src.handlers.liveness_handler import router as liveness_router
from src.handlers.flight_handler import router as flight_router
from src.middleware.rate_limiter import limiter, rate_limit_exceeded_handler
from src.middleware.error_handler import custom_exception_handler, general_exception_handler
from src.middleware.logging_middleware import LoggingMiddleware
from src.middleware.security_headers import SecurityHeadersMiddleware
from src.middleware.cors_middleware import setup_cors
from src.exceptions.base_exception import BaseCustomException


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Flight Booking API with Rate Limiting and Security",
        version=settings.APP_VERSION,
    )

    # Setup rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    
    # Setup error handlers
    app.add_exception_handler(BaseCustomException, custom_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Setup middleware (order matters - first added is outermost)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(LoggingMiddleware)
    setup_cors(app)

    # Include routers
    app.include_router(liveness_router)
    app.include_router(flight_router)

    @app.on_event("startup")
    async def startup_event():
        from src.logger import logger
        logger.info("Starting YetiAir API with security features...")
        logger.info(f"Rate limiting enabled: 100 requests/minute per IP")
        logger.info("Security headers enabled")

    @app.on_event("shutdown")
    async def shutdown_event():
        from src.logger import logger
        logger.info("Shutting down YetiAir API...")

    return app


app = create_app()
