from fastapi.responses import HTMLResponse
# main.py
from fastapi import FastAPI
from routers.api_v1.routers import router

app = FastAPI()
app.include_router(router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root():
    return '<a href="http://127.0.0.1:8000/api/v1/user">點擊這裡前往 user</a> \n <a href="http://127.0.0.1:8000/api/v1/data">點擊這裡前往 data</a'
