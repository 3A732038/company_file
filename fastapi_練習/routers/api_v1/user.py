# routers/user.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id):
    return {
        "message": f"用戶 {user_id} 的資訊",
        "user_id": user_id,
        "capabilities": [
            "查看用戶基本資訊",
            "檢查用戶權限等級",
            "查詢用戶所屬部門",
            "檢視用戶可存取的文件"
        ],
        "available_job_levels": ["regular", "senior", "manager", "director", "ceo"],
        "example_departments": ["hr", "engineering", "marketing", "sales"]
    }

@router.get("")
async def list_users():
    return {
        "message": "用戶管理系統",
        "description": "這個端點可以做甚麼？",
        "capabilities": [
            "管理企業用戶資訊",
            "查詢用戶權限等級",
            "檢視組織架構",
            "控制文件存取權限"
        ],
        "sample_users": [
            {"id": "ceo_wang", "level": "ceo", "department": "executive"},
            {"id": "tech_lead", "level": "manager", "department": "engineering"},
            {"id": "senior_engineer_john", "level": "senior", "department": "engineering"},
            {"id": "engineer_mary", "level": "regular", "department": "engineering"}
        ],
        "usage": "GET /api/v1/user/{user_id} 來查看特定用戶資訊"
    }
