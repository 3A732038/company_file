#!/bin/sh
# 容器進入點:先拉起常駐 headless LibreOffice,再用 uvicorn 跑 FastAPI 服務。
set -e
PORT="${SOFFICE_PORT:-2002}"

# 背景啟動 LibreOffice 監聽器(app.py 也會自我確認,這裡先熱機縮短首次轉檔延遲)
soffice --headless --invisible --nodefault --norestore --nologo \
  -env:UserInstallation=file:///tmp/louser \
  --accept="socket,host=localhost,port=${PORT};urp;" >/tmp/soffice.log 2>&1 &

cd /opt/ppt2pdf
exec uvicorn app:app --host 0.0.0.0 --port "${HTTP_PORT:-3000}"
