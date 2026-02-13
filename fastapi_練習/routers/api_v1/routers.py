# routers/routers.py
from fastapi import APIRouter
from routers.api_v1.user import router as user_router
from routers.api_v1.data import router as data_router
from routers.api_v1.notifications import router as notifications_router

router = APIRouter()

router.include_router(user_router, prefix="/user")
router.include_router(data_router, prefix="/data")
router.include_router(notifications_router, prefix="/notifications")