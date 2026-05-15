# =============================================
# Base: Python 3.12 + Node.js 18
# 用途: Claude Agent SDK + PPTX skill 環境
# =============================================
FROM python:3.12-slim

# --- 系統套件 ---
RUN apt-get update && apt-get install -y \
    # Node.js（Claude Code CLI + pptxgenjs 需要）
    nodejs \
    npm \
    # PPTX skill 轉圖片預覽用（可選，不需要可拿掉）
    libreoffice \
    poppler-utils \
    # 基本工具
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- Node.js 全域套件 ---
# Claude Code CLI（Agent SDK 的底層引擎，必裝）
RUN npm install -g @anthropic-ai/claude-code
# pptxgenjs（PPTX skill 從頭建立 PPT 用）
RUN npm install -g pptxgenjs

# --- Python 套件 ---
RUN pip install --no-cache-dir \
    # Claude Agent SDK（在 Python 裡控制 Claude Code）
    claude-agent-sdk \
    # FastAPI 後端
    fastapi \
    uvicorn \
    # PPTX skill 用
    Pillow \
    # 其他常用
    python-dotenv

# --- 工作目錄 ---
WORKDIR /app

# --- 複製你的後端程式 ---
COPY . .

# --- Skills 放這裡（之後可以 mount 進來）---
# COPY skills/ /app/skills/

# --- 不要在 Dockerfile 裡寫 API Key！---
# 用 docker run -e ANTHROPIC_API_KEY=xxx 或 docker-compose 傳入

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
