from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn


# 這段是 FastAPI 應用程式的生命週期管理：在同一個地方安排啟動時要做的事，以及關閉時要做的清理。概念上類似 Spring 的 @PostConstruct 和 @PreDestroy
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("研究 AI 應用程式啟動中")
    yield
    print("研究 AI 應用程式正在關閉")


# 建立 FastAPI 應用程式
app = FastAPI(title="Research AI Agent", version="1.0.0", lifespan=lifespan)

# 這會把 frontend 資料夾中的檔案掛載到 /static 路徑：
# • "/static"：網址的路徑前綴。
# • directory="frontend"：提供檔案的資料夾。
# • name="static"：FastAPI 內部用來辨識這個掛載項目的名稱。
app.mount("/static", StaticFiles(directory="frontend"), name="static", )


@app.get("/")
async def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    # 會啟動 Uvicorn 網路伺服器，讓它接收請求並交給 FastAPI 的 app 處理。
    uvicorn.run(app, host="0.0.0.0", port=8001)
