# ============================================================
#  PPT/Office -> PDF 轉檔服務(自帶中文字型 + 自動修跑版)
#  基底 gotenberg/gotenberg:8 取其現成的 LibreOffice + python-uno,
#  但「不」啟動 gotenberg server,改跑自己的 FastAPI 服務(app.py)。
# ============================================================
FROM gotenberg/gotenberg:8

USER root

# 1) 補字型:Noto CJK(思源)+ 微軟相容西文字型(開源、可散布)
RUN apt-get update && apt-get install -y --no-install-recommends \
      fonts-noto-cjk fonts-noto-cjk-extra \
      fonts-liberation fonts-crosextra-carlito \
    && rm -rf /var/lib/apt/lists/*

# 2) 複製 Windows 繁體中文原生字型(改善與 PowerPoint 的字型還原度)
#    msjh.ttc / msjhbd.ttc -> 微軟正黑體(Regular / Bold)
#    kaiu.ttf              -> 標楷體 (DFKai-SB)
#    mingliu.ttc           -> 新細明體 (PMingLiU) / 細明體
#    mingliub.ttc          -> 新細明體粗體
#    注:這些為 Microsoft 商業字型,僅供本機 / 內部使用,請勿對外散布 image。
COPY fonts/ /usr/share/fonts/truetype/win/

# 3) 重建字型快取,讓 LibreOffice 找得到上面的字型
RUN fc-cache -f

# 4) 裝 FastAPI / uvicorn(--ignore-installed 避開 Debian 既有套件的卸載衝突)
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip \
    && pip3 install --no-cache-dir --break-system-packages --ignore-installed \
         fastapi uvicorn python-multipart \
    && rm -rf /var/lib/apt/lists/*

# 5) 放入轉檔腳本與服務
COPY scripts/ /opt/ppt2pdf/
RUN chmod +x /opt/ppt2pdf/*.sh

EXPOSE 3000
USER gotenberg

# 取代 gotenberg 預設進入點,改跑自己的 PPT->PDF 服務
ENTRYPOINT ["/opt/ppt2pdf/entrypoint.sh"]
