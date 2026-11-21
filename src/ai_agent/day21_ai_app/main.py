from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
import uvicorn

from schemas import ChatRequest, ChatResponse
from agent import run_agent


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


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 檢查請求是否有消息
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="訊息不可為空。")

    try:
        # 1. 呼叫 run_agent 函數，傳入請求的訊息，並等待回應；run_in_threadpool 會把同步函式交給背景執行緒執行。
        result = await run_in_threadpool(run_agent, request.message)

        # 2. 回應請求
        return ChatResponse(response=result)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    # 會啟動 Uvicorn 網路伺服器，讓它接收請求並交給 FastAPI 的 app 處理。
    uvicorn.run(app, host="0.0.0.0", port=8001)
