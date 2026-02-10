from fastapi import FastAPI
from src.config import settings
from src.handlers.liveness_handler import router as liveness_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="Flight Booking API",
        version=settings.APP_VERSION,
    )

    # Include routers
    app.include_router(liveness_router)

    return app

app = create_app()
