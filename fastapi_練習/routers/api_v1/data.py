# routers/data.py
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def root():
    return {"message": "get data"}

@router.post("")
async def root():
    return {"message": "Hello World"}