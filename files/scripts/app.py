#!/usr/bin/env python3
"""PPT/Office -> PDF 轉檔服務(FastAPI web 層)。

注意:本檔「不」import uno。LibreOffice 的 uno.py 會攔截 import 機制,
與 uvicorn 的選擇性匯入衝突,故轉檔一律交給獨立 process(worker.py)。

端點(與 gotenberg 相容):
  POST /forms/libreoffice/convert   (-F files=@x.pptx)   亦提供別名 POST /convert
  GET  /health
"""
import os
import sys
import threading
import tempfile
import subprocess
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response, PlainTextResponse

WORKER = os.environ.get("WORKER_SCRIPT", "/opt/ppt2pdf/worker.py")
SOFFICE_PORT = os.environ.get("SOFFICE_PORT", "2002")
_lock = threading.Lock()                 # 單一 LibreOffice -> 串行化轉檔

app = FastAPI(title="PPT/Office to PDF", docs_url="/docs")


@app.get("/health", response_class=PlainTextResponse)
def health():
    return "ok"


@app.post("/forms/libreoffice/convert")
@app.post("/convert")
def convert_endpoint(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="no file uploaded")
    upload = files[0]
    with tempfile.TemporaryDirectory() as d:
        in_path = os.path.join(d, upload.filename or "in.pptx")
        out_path = os.path.join(d, "out.pdf")
        with open(in_path, "wb") as f:
            f.write(upload.file.read())

        with _lock:
            r = subprocess.run(
                [sys.executable, WORKER, in_path, out_path, SOFFICE_PORT],
                capture_output=True, text=True, timeout=300)
        if r.returncode != 0 or not os.path.exists(out_path):
            raise HTTPException(
                status_code=500,
                detail="convert failed: " + (r.stderr or r.stdout or "unknown"))

        with open(out_path, "rb") as f:
            pdf = f.read()

    headers = {"Content-Disposition": 'attachment; filename="output.pdf"'}
    return Response(content=pdf, media_type="application/pdf", headers=headers)
