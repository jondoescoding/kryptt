from fastapi import APIRouter
from .settings import router as settings_router

router = APIRouter(prefix="/v1")
router.include_router(settings_router)
