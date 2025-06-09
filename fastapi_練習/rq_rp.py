# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import StreamingResponse
# import pandas as pd
# import io

# app = FastAPI()

# @app.post("/csv")
# async def read_users(file: UploadFile = File(...)):
#     file_buffer = await file.read()
#     file_object = io.BytesIO(file_buffer)
#     df = pd.read_csv(file_object)

#     # do something
#     new_file_buffer = df.to_csv(index=False)

#     def iterator(buffer):
#         yield buffer

#     return StreamingResponse(iterator(new_file_buffer), media_type="text/csv")

    


from fastapi import FastAPI, UploadFile, File
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,HTMLResponse  
import os
import base64
app = FastAPI(title="MNIST 分類器")

FORMAT = "%(asctime)s %(levelname)s [%(filename)s] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

app.mount("/static", StaticFiles(directory="."), name="static")
    
@app.get("/", response_class=FileResponse)
async def home():
    file_path = "web/test.html"
    if os.path.exists(file_path):   
        return FileResponse(file_path)
    return "<h2>找不到網頁檔案！</h2>"

@app.post("/api/v1/mnist", response_class=HTMLResponse)
async def mnist_classifier(file: UploadFile = File(...)):
    try:
        file_location = f"./temp.jpg"
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        file.file.seek(0)  # 確保後續讀取仍可用    
        encoded_image = base64.b64encode(file.file.read()).decode("utf-8")
        image_type = file.content_type  
        logging.info(f"圖片類型 {image_type}")
        logging.info(f"成功上傳 {file.filename}")
        return HTMLResponse(content=f'''
        <h2>上傳成功!!!!</h2>
        <p>檔案名稱: {file.filename}</p>
        <img src="data:{image_type};base64,{encoded_image}" alt="Uploaded Image">
        ''')

    except Exception as e:
        logging.error(e)
        return {"error": "上傳失敗"}
