# 企業文件管理與權限控制系統

## 你可以做甚麼事情？

這個系統提供企業級的文件管理和權限控制功能，結合了現代 Web API 技術和強大的權限控制機制。

## 🚀 快速開始

### 啟動主要 API 服務
```bash
cd fastapi_練習
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 啟動文件上傳服務
```bash
cd fastapi_練習  
uvicorn rq_rp:app --host 0.0.0.0 --port 8001 --reload
```

### 訪問系統
- 主頁面: http://localhost:8000/
- 功能總覽: http://localhost:8000/capabilities
- API 文檔: http://localhost:8000/docs
- 文件上傳: http://localhost:8001/

## 🔐 核心功能

### 1. 文件權限控制系統 (SpiceDB)
- **5級安全等級**: L1(公開) → L2(資深) → L3(經理) → L4(總監) → L5(CEO)
- **職級階層管理**: 完整的組織階層從一般員工到 CEO
- **組織結構權限**: 部門、專案、組織層級的細緻權限控制
- **文件分類管理**: 支援各種企業文件類型的權限管理

#### 檔案位置
- `SPICEDB_複雜版/document_classification_schema.txt` - 權限控制架構定義
- `SPICEDB_複雜版/document_classification_examples.sh` - 實際權限設定範例

### 2. Web API 功能
- **用戶管理**: `/api/v1/user` - 企業用戶資訊管理
- **數據處理**: `/api/v1/data` - 數據分析與處理服務
- **文件上傳**: 支援圖片和文件上傳處理
- **RESTful API**: 完整的 HTTP 方法支援

### 3. 文件處理能力
- **圖片處理**: MNIST 圖片分類功能
- **數據處理**: pandas, numpy 支援的數據分析
- **文件上傳**: 多格式文件上傳與處理
- **Base64 編碼**: 圖片編碼與即時顯示

### 4. 組織管理功能
- **部門管理**: HR、工程、行銷、業務等部門
- **專案管理**: 專案成員與權限分配
- **角色控制**: 管理員、編輯者、檢視者等多種角色
- **權限繼承**: 階層式權限自動繼承機制

## 📋 API 端點說明

| 端點 | 方法 | 功能描述 |
|------|------|----------|
| `/` | GET | 系統主頁面 |
| `/capabilities` | GET | 完整功能說明頁面 |
| `/capabilities/json` | GET | JSON 格式的功能列表 |
| `/api/v1/user` | GET | 用戶管理系統總覽 |
| `/api/v1/user/{user_id}` | GET | 查看特定用戶資訊 |
| `/api/v1/data` | GET | 數據處理系統說明 |
| `/api/v1/data` | POST | 處理上傳的數據 |

## 🛠️ 技術架構

### 後端技術
- **FastAPI**: 高效能 Python Web 框架
- **SpiceDB**: Google Zanzibar 風格的權限控制系統
- **Uvicorn**: ASGI 服務器
- **Pydantic**: 數據驗證與序列化

### 數據處理
- **pandas**: 數據分析與處理
- **numpy**: 數值計算
- **Python**: 主要開發語言

### 部署支援
- **Docker**: 容器化部署支援
- **pipenv**: Python 環境管理

## 💼 使用案例

### 企業文件管理
```bash
# 查看系統能處理的文件類型
curl http://localhost:8000/capabilities/json

# 查看用戶權限
curl http://localhost:8000/api/v1/user/tech_lead
```

### 權限控制範例
系統支援以下權限控制場景：
- CEO 可存取所有等級文件 (L1-L5)
- 總監可存取 L1-L4 等級文件
- 經理可存取 L1-L3 等級文件
- 資深員工可存取 L1-L2 等級文件
- 一般員工僅可存取 L1 等級文件

### 數據處理
```bash
# 查看數據處理能力
curl http://localhost:8000/api/v1/data

# 處理數據 (POST)
curl -X POST http://localhost:8000/api/v1/data
```

## 📁 專案結構

```
company_file/
├── SPICEDB_複雜版/           # SpiceDB 權限控制系統
│   ├── document_classification_schema.txt
│   └── document_classification_examples.sh
├── fastapi_練習/             # FastAPI 應用程式
│   ├── main.py              # 主要 API 服務
│   ├── rq_rp.py             # 文件上傳服務
│   ├── routers/             # API 路由
│   └── web/                 # 前端頁面
├── spicedb操作/              # SpiceDB 配置文件
└── requirements.txt         # Python 依賴
```

## 🔧 開發指南

### 安裝依賴
```bash
pip install fastapi uvicorn python-multipart pandas numpy
```

### 開發模式啟動
```bash
# 主服務 (含自動重載)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 文件服務
uvicorn rq_rp:app --reload --host 0.0.0.0 --port 8001
```

### 添加新功能
1. 在 `routers/api_v1/` 目錄下創建新的路由文件
2. 在 `routers/api_v1/routers.py` 中註冊新路由
3. 更新權限控制配置 (如需要)

## 📞 API 範例

### 查詢系統功能
```bash
curl -X GET http://localhost:8000/capabilities/json | jq .
```

### 用戶管理
```bash
# 列出所有用戶功能
curl -X GET http://localhost:8000/api/v1/user | jq .

# 查看特定用戶
curl -X GET http://localhost:8000/api/v1/user/ceo_wang | jq .
```

### 數據處理
```bash
# 查看數據處理功能
curl -X GET http://localhost:8000/api/v1/data | jq .

# 提交數據處理請求
curl -X POST http://localhost:8000/api/v1/data | jq .
```

---

## 總結：你可以做甚麼事情？

這個系統讓你能夠：
1. **管理企業文件權限** - 透過 SpiceDB 實現細緻的權限控制
2. **處理各種數據** - 支援 CSV、JSON 等格式的數據分析
3. **管理用戶與組織** - 完整的企業組織架構管理
4. **上傳與處理文件** - 支援圖片、文檔等多種文件類型
5. **提供 Web API 服務** - RESTful API 支援各種應用整合
6. **部署企業級應用** - 可擴展的微服務架構

適用於需要嚴格權限控制和數據處理能力的企業環境。