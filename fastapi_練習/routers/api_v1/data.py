# routers/data.py
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_data():
    return {
        "message": "數據處理系統",
        "description": "這個端點可以做甚麼？",
        "capabilities": [
            "處理 CSV 數據文件",
            "執行數據分析與統計",
            "生成數據報表",
            "支援 pandas 數據操作"
        ],
        "supported_formats": ["CSV", "JSON", "Excel"],
        "data_processing_features": [
            "數據清理與轉換",
            "統計分析",
            "數據視覺化",
            "批量數據處理"
        ],
        "usage": "POST /api/v1/data 來上傳和處理數據"
    }

@router.post("")
async def process_data():
    return {
        "message": "數據處理完成",
        "description": "POST 端點可以處理上傳的數據",
        "processing_capabilities": [
            "接收 JSON 或 CSV 數據",
            "執行數據驗證",
            "進行數據轉換",
            "返回處理結果"
        ],
        "example_operations": [
            "計算統計數據",
            "數據格式轉換",
            "數據品質檢查",
            "生成數據摘要"
        ]
    }