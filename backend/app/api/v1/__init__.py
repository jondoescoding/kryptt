from fastapi import APIRouter
from .settings import router as settings_router
from .alpaca import router as alpaca_router

router = APIRouter(prefix="/v1")
router.include_router(settings_router)
router.include_router(alpaca_router)
