from fastapi import FastAPI
from src.config import settings
from src.handlers.liveness_handler import router as liveness_router
from src.handlers.flight_handler import router as flight_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Flight Booking API",
        version=settings.APP_VERSION,
    )

    # Include routers
    app.include_router(liveness_router)
    app.include_router(flight_router)

    @app.on_event("startup")
    async def startup_event():
        from src.logger import logger
        logger.info("Starting YetiAir API...")

    return app

app = create_app()
