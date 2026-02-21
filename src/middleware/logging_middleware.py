"""Request/Response logging middleware."""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        """Log request and response details."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} - Duration: {duration:.3f}s",
            extra={
                "status_code": response.status_code,
                "duration": duration,
                "path": request.url.path
            }
        )
        
        return response
