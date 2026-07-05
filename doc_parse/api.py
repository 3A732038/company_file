# -*- coding: utf-8 -*-
"""
Web API：使用者上傳檔案 → 解析 → 回傳 markdown 給 LLM 用。一次性、零殘留。

啟動：
  .venv\\Scripts\\uvicorn.exe api:app --host 0.0.0.0 --port 8080

前端呼叫（multipart/form-data，欄位名 files，可多檔）：
  POST /parse  →  {"markdown": "..."}   ← 直接塞進 LLM prompt

設計：
  - 上傳檔只暫存到解析完成，圖片全程在記憶體送 VLM，
    請求結束整包刪除 → 不佔磁碟、沒有隱私殘留
  - 解析是 CPU 密集，端點用同步 def → FastAPI 自動丟 threadpool
"""
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

import doc_parser

app = FastAPI(title="文件解析服務")

TMP_ROOT = Path("output")   # 暫存根目錄（正常情況下請求結束即空）


@app.post("/parse")
def parse(files: list[UploadFile]):
    doc_parser.cleanup_old_outputs()        # 撈漏網之魚（伺服器中途掛掉留下的）

    tmp_dir = TMP_ROOT / uuid.uuid4().hex[:12]
    tmp_dir.mkdir(parents=True)
    try:
        saved = []
        for f in files:
            name = Path(f.filename or "").name      # 去除路徑，防目錄跳脫
            # 修復非 UTF-8 客戶端（如 Windows curl 用 cp950）的檔名亂碼；
            # 瀏覽器上傳一律 UTF-8，不會走到修復
            try:
                raw = name.encode("latin-1")
                for enc in ("utf-8", "cp950"):
                    try:
                        name = raw.decode(enc)
                        break
                    except UnicodeDecodeError:
                        continue
            except UnicodeEncodeError:
                pass                                # 已是正常 Unicode 檔名
            if not name:
                continue
            dest = tmp_dir / name
            dest.write_bytes(f.file.read())
            saved.append(dest)
        if not saved:
            raise HTTPException(400, "沒有收到檔案")

        try:
            combined, _ = doc_parser.process_many(saved, persist=False)
        except ValueError as e:                     # 不支援的格式 → 400
            raise HTTPException(400, str(e))

        return {"markdown": combined}
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)  # 一次性：用完即刪


@app.get("/health")
def health():
    return {"status": "ok"}
