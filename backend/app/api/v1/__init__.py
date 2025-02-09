from fastapi import APIRouter
from .settings import router as settings_router
from .alpaca import router as alpaca_router
from .assets import router as assets_router
from .position import router as position_router

router = APIRouter(prefix="/v1")
router.include_router(settings_router)
router.include_router(alpaca_router)
router.include_router(assets_router)
router.include_router(position_router)
