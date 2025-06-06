# routers/routers.py
from fastapi import APIRouter
from routers.api_v1.user import router as user_router
from routers.api_v1.data import router as data_router

router = APIRouter()

router.include_router(user_router, prefix="/user")
router.include_router(data_router, prefix="/data")