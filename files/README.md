# PPT/Office → PDF 轉檔服務(FastAPI + 自帶字型 + 自動修跑版)

以 LibreOffice 轉檔,並在轉檔前自動修正最常見的「跑版/溢出」問題:
文字框因字型替換、行高差異而**往下長**,導致**撐破投影片下緣**或**疊到其他圖形**。
作法是把這類「自動長高」的文字框改成「**固定高度 + 縮小文字以符合**」(含群組內的文字框)。

## 內容

| 檔案 | 說明 |
|------|------|
| `Dockerfile` | 基於 `gotenberg/gotenberg:8`,加字型 + FastAPI + 腳本,改跑自己的服務 |
| `docker-compose.yml` | 一鍵啟動服務(對外 3001) |
| `fonts/` | 中文字型(微軟正黑體、標楷體、新細明體) |
| `scripts/app.py` | FastAPI web 層(不碰 uno) |
| `scripts/worker.py` | 跑版修正 + 輸出 PDF(python-UNO);獨立 process 執行,也可當 CLI |
| `scripts/entrypoint.sh` | 進入點:熱機 LibreOffice + 啟動 uvicorn |
| `scripts/convert.sh` | CLI 轉檔(供 `docker exec` 用) |

> 為何 web 與 worker 分開:LibreOffice 的 `uno.py` 會攔截 Python import 機制,
> 與 uvicorn 的選擇性匯入衝突,因此 web 層不能 import uno,轉檔改由子行程 `worker.py` 處理。

## 建置與啟動

```bash
docker compose up -d --build
curl http://localhost:3001/health      # 回 ok 即就緒
```

## 轉檔

HTTP(與 gotenberg 相容的 `-F files=@` 介面,既有呼叫幾乎不用改):

```bash
curl -X POST -F files=@來源.pptx http://localhost:3001/forms/libreoffice/convert -o 輸出.pdf
# 簡短別名亦可:POST /convert
```

API 文件:`http://localhost:3001/docs`

或 CLI(把檔案放進掛載目錄,再 exec):

```bash
docker exec ppt2pdf /opt/ppt2pdf/convert.sh /data/來源.pptx /data/輸出.pdf
```

## 字型授權(重要)

`fonts/` 內的微軟正黑體 / 標楷體 / 新細明體為 **Microsoft 商業字型**,
僅供**內部 / 本機**使用,**請勿把 image 推到公開 registry 或對外散布**。
若需公開散布,請改用開源字型(Noto CJK、教育部標楷體 TW-Kai、AR PL UMing)取代 `fonts/`。

## 限制(誠實說明)

- 修正手法是「縮小文字」,出問題的框字會略小(多數情況與 PowerPoint 的 autofit 行為一致)。
- **修不到**:圖片/圖表本身超出、表格溢出、PPT 原檔就有的問題。
- 用 LibreOffice 轉檔**先天無法**與 PowerPoint 100% 像素一致;要求精準的檔案請轉後抽查,或改用 PowerPoint 轉。
- 服務為**單一 LibreOffice 實例、串行轉檔**(測試級)。高並發請啟動多個容器副本,前面擺負載平衡。
