import asyncio
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions

app = FastAPI()

# Skills 和輸出目錄
SKILLS_DIR = Path("/app/skills")
OUTPUT_DIR = Path("/app/outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class PPTRequest(BaseModel):
    topic: str        # 使用者輸入的主題
    slides: int = 5   # 想要幾頁


@app.post("/generate-ppt")
async def generate_ppt(req: PPTRequest):
    output_path = OUTPUT_DIR / f"{req.topic}.pptx"

    # 讀取 PPTX skill 的說明（當作 system prompt 的一部分）
    skill_prompt = ""
    skill_md = SKILLS_DIR / "pptx" / "SKILL.md"
    if skill_md.exists():
        skill_prompt = skill_md.read_text()

    prompt = f"""
{skill_prompt}

請幫我製作一份關於「{req.topic}」的簡報，共 {req.slides} 頁。
輸出檔案存到：{output_path}
"""

    # 用 Claude Agent SDK 驅動 Claude Code 執行
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash", "Glob"],
            permission_mode="bypassPermissions",  # 容器裡全自動，不需要人工確認
            cwd=str(OUTPUT_DIR),
        ),
    ):
        pass  # 可以在這裡 stream 進度給前端

    return FileResponse(
        path=output_path,
        filename=f"{req.topic}.pptx",
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )


@app.get("/health")
def health():
    return {"status": "ok"}
