# -*- coding: utf-8 -*-
"""
VLM 接口 —— 之後接模型只需要改這個檔案。

doc_parser.py 會呼叫 describe_images(items)，
items 是一串 ImageItem（見 doc_parser.py），每個有：
    item.filename  圖片存檔路徑（相對 output 資料夾）
    item.abs_path  圖片絕對路徑
    item.context   圖片周圍的文字（拿來當提示，讓 VLM 描述更準）
    item.description  ← 你要填回去的欄位

接好模型後把 VLM_ENABLED 改成 True，並填好下面的設定。
"""

VLM_ENABLED = False          # ← 接好模型後改 True
VLM_BASE_URL = "http://localhost:8000/v1"   # ← 你的 vLLM 端點
VLM_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"   # ← 你的模型名
VLM_API_KEY = "EMPTY"
MAX_CONCURRENT = 8           # 併發上限（對齊你 GPU 的甜蜜點）
MAX_TOKENS = 200             # 單圖描述：短一點快很多
MAX_TOKENS_FULLPAGE = 600    # 整頁判讀：內容多，給多一點


def describe_images(items):
    """對過濾後的圖片批次產生描述，把結果寫回 item.description。"""
    if not VLM_ENABLED:
        for it in items:
            it.description = "（VLM 未接，待補圖片描述）"
        return

    import asyncio
    asyncio.run(_batch_describe(items))


async def _batch_describe(items):
    """AsyncOpenAI + semaphore 併發送出 → vLLM 端自動 batch。"""
    import base64
    from openai import AsyncOpenAI

    client = AsyncOpenAI(base_url=VLM_BASE_URL, api_key=VLM_API_KEY)
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def one(it):
        async with sem:
            b64 = base64.b64encode(it.data).decode()   # 直接用記憶體資料，不落地
            if it.is_full_page:
                # 模式3：整頁判讀 —— 重點是圖文「對應關係」
                prompt = ("這是文件完整的一頁。請用繁體中文完整判讀：頁面上的文字、"
                          "每張圖片/圖表的內容，以及圖片與文字的對應關係"
                          "（例如哪張圖對應哪個標題或說明）。若有表格請讀出數據。")
                if it.context:
                    prompt += f"\n此頁抽取出的文字層供對照：{it.context[:500]}"
            else:
                prompt = "用繁體中文簡短描述這張圖的內容（若是圖表請讀出關鍵數據）。"
                if it.context:
                    prompt += f"\n圖片周圍的文字供參考：{it.context[:300]}"
            resp = await client.chat.completions.create(
                model=VLM_MODEL,
                max_tokens=MAX_TOKENS_FULLPAGE if it.is_full_page else MAX_TOKENS,
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/png;base64,{b64}"}},
                ]}],
            )
            it.description = resp.choices[0].message.content.strip()

    await asyncio.gather(*[one(it) for it in items])
