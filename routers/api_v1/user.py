# routers/user.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}")
async def root(user_id):
    return {"message": f"Hello user {user_id}"}

@router.get("")
async def root():
    return {"message": "Hello World"}
