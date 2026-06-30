#!/bin/sh
# CLI 轉檔(不經 HTTP)。用法:
#   docker exec <容器> /opt/ppt2pdf/convert.sh /data/來源.pptx /data/輸出.pdf
# app.py 內部會自行確認/啟動 headless LibreOffice。
set -e
IN="$1"
OUT="$2"

if [ -z "$IN" ] || [ -z "$OUT" ]; then
  echo "usage: convert.sh <input.pptx> <output.pdf>" >&2
  exit 2
fi

exec python3 /opt/ppt2pdf/worker.py "$IN" "$OUT"
