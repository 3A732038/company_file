from fastapi.responses import HTMLResponse
# main.py
from fastapi import FastAPI
from routers.api_v1.routers import router

app = FastAPI(title="Company File Management System", description="企業文件管理與權限控制系統")
app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root():
    return '''
    <html>
    <head><title>企業文件管理系統</title><meta charset="UTF-8"></head>
    <body>
        <h1>企業文件管理系統 - 功能總覽</h1>
        <h2>你可以做甚麼事情？</h2>
        <ul>
            <li><a href="/capabilities">📋 查看系統完整功能列表</a></li>
            <li><a href="/api/v1/user">👤 用戶管理功能</a></li>
            <li><a href="/api/v1/data">📊 數據處理功能</a></li>
            <li><a href="/docs">📖 API 文檔</a></li>
        </ul>
    </body>
    </html>
    '''

@app.get("/capabilities", response_class=HTMLResponse)
async def capabilities():
    return '''
    <html>
    <head><title>系統功能總覽</title><meta charset="UTF-8"></head>
    <body>
        <h1>你可以做甚麼事情？系統功能總覽</h1>
        
        <h2>🔐 文件權限控制系統 (SpiceDB)</h2>
        <ul>
            <li><strong>5級安全等級分類</strong>: L1(公開) → L2(資深) → L3(經理) → L4(總監) → L5(CEO)</li>
            <li><strong>職級階層管理</strong>: 一般員工 → 資深員工 → 經理 → 總監 → CEO</li>
            <li><strong>組織結構權限</strong>: 部門、專案、組織層級的權限控制</li>
            <li><strong>文件分類管理</strong>: 公司手冊、技術文件、預算資料、策略文件等</li>
        </ul>

        <h2>🌐 Web API 功能</h2>
        <ul>
            <li><strong>用戶管理</strong>: <a href="/api/v1/user">用戶資訊查詢與管理</a></li>
            <li><strong>數據處理</strong>: <a href="/api/v1/data">數據操作與處理</a></li>
            <li><strong>文件上傳</strong>: 支援圖片上傳與處理</li>
            <li><strong>RESTful API</strong>: 完整的 HTTP 方法支援</li>
        </ul>

        <h2>📁 文件處理能力</h2>
        <ul>
            <li><strong>圖片處理</strong>: MNIST 圖片分類</li>
            <li><strong>CSV 數據處理</strong>: pandas 數據分析</li>
            <li><strong>Base64 編碼</strong>: 圖片編碼與顯示</li>
            <li><strong>靜態文件服務</strong>: HTML、CSS、圖片等靜態資源</li>
        </ul>

        <h2>👥 組織管理功能</h2>
        <ul>
            <li><strong>部門管理</strong>: HR、工程、行銷、業務部門</li>
            <li><strong>專案管理</strong>: 專案成員與權限控制</li>
            <li><strong>角色分配</strong>: 管理員、編輯者、檢視者等角色</li>
            <li><strong>權限繼承</strong>: 階層式權限繼承機制</li>
        </ul>

        <h2>🔧 技術能力</h2>
        <ul>
            <li><strong>FastAPI 框架</strong>: 高效能 Python Web 框架</li>
            <li><strong>SpiceDB</strong>: Google Zanzibar 風格的權限控制</li>
            <li><strong>數據科學</strong>: pandas, numpy 數據處理</li>
            <li><strong>容器化部署</strong>: Docker 支援</li>
        </ul>

        <p><a href="/">⬅️ 回到首頁</a></p>
    </body>
    </html>
    '''

@app.get("/capabilities/json")
async def capabilities_json():
    """API 格式的系統功能列表"""
    return {
        "question": "你可以做甚麼事情？",
        "answer": "本系統具備以下功能",
        "capabilities": {
            "document_access_control": {
                "name": "文件權限控制系統",
                "features": [
                    "5級安全等級分類 (L1-L5)",
                    "職級階層管理 (員工-CEO)",
                    "組織結構權限控制",
                    "文件分類管理"
                ]
            },
            "web_api": {
                "name": "Web API 功能", 
                "features": [
                    "用戶管理",
                    "數據處理",
                    "文件上傳",
                    "RESTful API"
                ]
            },
            "file_processing": {
                "name": "文件處理能力",
                "features": [
                    "圖片處理 (MNIST)",
                    "CSV 數據處理",
                    "Base64 編碼",
                    "靜態文件服務"
                ]
            },
            "organization_management": {
                "name": "組織管理功能",
                "features": [
                    "部門管理",
                    "專案管理", 
                    "角色分配",
                    "權限繼承"
                ]
            },
            "technical_stack": {
                "name": "技術能力",
                "features": [
                    "FastAPI 框架",
                    "SpiceDB 權限控制",
                    "數據科學工具",
                    "容器化部署"
                ]
            }
        }
    }
