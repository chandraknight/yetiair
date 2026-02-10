from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def liveness_check():
    return {"status": "ok"}
