from fastapi import FastAPI, HTTPException
import httpx  # 匯入 HTTPX，讓 /ready 可以用 httpx.AsyncClient() 向 Ollama 發送非同步 HTTP 請求。
from contextlib import asynccontextmanager  # 匯入裝飾器，讓下面的 lifespan() 函式成為非同步 context manager。yield 前的程式在應用程式啟動時執行；yield 後的程式在應用程式關閉時執行。

from schemas import ChatRequest, ChatResponse  # 輸入的資料格式

from model import OLLAMA_BASE_URL
from agent import agent


# 這段是 FastAPI 應用程式的生命週期管理：在同一個地方安排啟動時要做的事，以及關閉時要做的清理。概念上類似 Spring 的 @PostConstruct 和 @PreDestroy
@asynccontextmanager
async def lifespan(app: FastAPI):
    # app: FastAPI 的意思是：這個參數叫 app（可任意命名），它的預期型別是 FastAPI 應用程式物件。
    # 因為你把 lifespan 傳給了 FastAPI(lifespan=lifespan)，FastAPI 在應用程式啟動時會把目前的 app 物件傳入這個函式。
    print("應用程式啟動中...")  # yield 前的程式在應用程式啟動時執行
    yield
    print("應用程式正在關閉...")  # yield 後的程式在應用程式關閉時執行


# 這行建立一個 FastAPI 應用程式物件，並把它指定給 app。同一個檔案接著用 app.post("/chat") 在這個應用程式上註冊 /chat 路由。
app = FastAPI(title="AI Agent API", version="1.0.0", lifespan=lifespan)


# request: ChatRequest 表示 request 這個參數的型別是 ChatRequest。呼叫 /chat 時，FastAPI 會先把收到的 JSON body 解析並驗證，再建立 ChatRequest 物件交給函式。
# response_model=ChatResponse 告訴 FastAPI：這個 API 回傳給呼叫者的資料，應該符合 ChatResponse 格式。你的 ChatResponse 定義是：
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):  # ChatRequest : {"message": "你好"}
    try:
        # 1. 呼叫 agent.ainvoke() 執行 agent，取得執行結果
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.message  # FastAPI 已先驗證 request body
                    }
                ]
            }
        )
        # 2. 取得 agent 最後一則訊息的內容
        answer = result["messages"][-1].content
        # 3. 將答案包裝成 ChatResponse 並回傳
        return ChatResponse(answer=answer)

    except Exception as exc:
        print(f"Agent 執行失敗：{exc}")
        raise HTTPException(status_code=500, detail="Agent 執行失敗_HTTP_500")
        # detail = 設定要回傳給呼叫者的錯誤訊息。客戶端會收到類似這樣的內容


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


@app.get("/ready")
async def ready():
    try:
        # • httpx.AsyncClient()：建立可用於非同步 HTTP 請求的 client。
        # • async with：進入區塊時開啟 client，離開時自動關閉。
        async with httpx.AsyncClient() as client:
            # Ollama 會用這個端點列出本機可用的模型．Ollama 會用這個端點列出本機可用的模型
            response = await client.get(
                f"{OLLAMA_BASE_URL.rstrip('/')}/api/tags",
                timeout=2.0
            )

        if response.status_code == 200:
            return {
                "status": "ready"
            }

        return {
            "status": "not_ready"
        }

    except Exception:
        return {
            "status": "not_ready"
        }

# async with httpx.AsyncClient() as client:
#     response = await client.get(...) # 離開區塊後，client 已關閉

# same as

# client = httpx.AsyncClient()
# try:
#     response = await client.get(...)
# finally:
#     await client.aclose()
