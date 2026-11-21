from fastapi import FastAPI, HTTPException, Request
import httpx  # 匯入 HTTPX，讓 /ready 可以用 httpx.AsyncClient() 向 Ollama 發送非同步 HTTP 請求。
from contextlib import asynccontextmanager  # 匯入裝飾器，讓下面的 lifespan() 函式成為非同步 context manager。yield 前的程式在應用程式啟動時執行；yield 後的程式在應用程式關閉時執行。
from schemas import ChatRequest, ChatResponse  # 輸入的資料格式

import asyncio
import logging
import time
import uuid
from collections import defaultdict, deque
from tenacity import retry, stop_after_attempt, wait_exponential

from model import OLLAMA_BASE_URL
from agent import agent

# 設定 logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("ai_agent")

REQUEST_LIMIT = 10
WINDOW_SECONDS = 60

# request_times =
# {
#     "client_A": deque([1000.0, 1012.5]),
#     "client_B": deque([1008.3]),
# }
request_times = defaultdict(deque)


# 這段是 FastAPI 應用程式的生命週期管理：在同一個地方安排啟動時要做的事，以及關閉時要做的清理。概念上類似 Spring 的 @PostConstruct 和 @PreDestroy
@asynccontextmanager
async def lifespan(app: FastAPI):
    # app: FastAPI 的意思是：這個參數叫 app（可任意命名），它的預期型別是 FastAPI 應用程式物件。
    # 因為你把 lifespan 傳給了 FastAPI(lifespan=lifespan)，FastAPI 在應用程式啟動時會把目前的 app 物件傳入這個函式。
    print("應用程式啟動中...")  # yield 前的程式在應用程式啟動時執行
    yield
    print("應用程式正在關閉...")  # yield 後的程式在應用程式關閉時執行


@retry(
    stop=stop_after_attempt(2),  # 最多執行 2 次
    wait=wait_exponential(multiplier=1, min=1, max=4)  # 等待時間分別為 1, 2, 4 秒
)
async def run_agent(message: str):
    return await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )


# 每個 client_id 在最近 60 秒內最多允許 10 次請求。
# • 回傳 True：請求次數未達上限，這次請求時間也會被記錄。
# • 回傳 False：最近 60 秒內已記錄 10 次，這次請求應被拒絕。
def check_rate_limit(client_id: str) -> bool:
    now = time.time()

    # request_times = {
    #     "client_A": deque([1000.0, 1012.5]),
    #     "client_B": deque([1008.3]),
    # }

    # times = request_times["client_A"] = deque([1000.0, 1012.5])
    times = request_times[client_id]

    # 檢查最早的請求是否已超過 60 秒 (times：檢查 deque 是否有元素)
    while times and now - times[0] > WINDOW_SECONDS:
        times.popleft()  # 從 deque 左邊移除過期時間。因為時間依序加入，最舊的請求在最左邊；如果它已過期，就繼續檢查下一筆。

    # 若清除過期時間後，仍有 10 筆或更多記錄，回傳 False，拒絕這次請求。
    if len(times) >= REQUEST_LIMIT:
        return False

    # 否則用 times.append(now) 把這次請求時間加到右邊，回傳 True，表示允許。
    times.append(now)
    return True


# 這行建立一個 FastAPI 應用程式物件，並把它指定給 app。同一個檔案接著用 app.post("/chat") 在這個應用程式上註冊 /chat 路由。
app = FastAPI(title="AI Agent API", version="1.0.0", lifespan=lifespan)


# body: ChatRequest 表示 body 這個參數的型別是 ChatRequest。呼叫 /chat 時，FastAPI 會先把收到的 JSON body 解析並驗證，再建立 ChatRequest 物件交給函式。
# response_model=ChatResponse 告訴 FastAPI：這個 API 回傳給呼叫者的資料，應該符合 ChatResponse 格式。你的 ChatResponse 定義是：
@app.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):  # ChatRequest : {"message": "你好"}

    request_id = str(uuid.uuid4())  # 生成一筆 UUID 作為 request_id

    client_id = request.client.host  # 取得 client 位址

    # 檢查請求速率限制
    if not check_rate_limit(client_id):
        logger.warning("超出請求速率限制 request_id=%s client=%s", request_id, client_id)
        raise HTTPException(status_code=429, detail="請求速率超出限制")

    # 記錄請求開始時間
    start_time = time.perf_counter()
    logger.info("請求開始 request_id=%s", request_id)

    try:
        # 1. 呼叫 run_agent() 執行 agent，最多等待 30 秒；逾時時 asyncio.wait_for() 會丟出 asyncio.TimeoutError。
        result = await asyncio.wait_for(run_agent(body.message), timeout=30)
        # 2. 取得 agent 最後一則訊息的內容
        answer = result["messages"][-1].content

        duration = time.perf_counter() - start_time
        logger.info("請求完成 request_id=%s 耗時=%.2f秒", request_id, duration)

        # 3. 將答案包裝成 ChatResponse 並回傳
        return ChatResponse(answer=answer)

    except asyncio.TimeoutError:
        logger.error("請求逾時 request_id=%s", request_id)
        raise HTTPException(status_code=504, detail="Agent 請求逾時")

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
