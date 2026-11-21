from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
import uvicorn
# Uvicorn 的 event loop 執行緒
#  ├─ 執行 event_stream
#  ├─ 等待 queue.get()
#  └─ 執行 callback，把 event 放進 Queue
import asyncio
import json

from schemas import ChatRequest, ChatResponse
from agent import run_agent, research_agent


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


# Create the event stream
# 1. 瀏覽器呼叫 /research?topic=...。
# 2. research() 建立 Queue 和 progress_callback。callback 的工作是把研究進度放進 Queue。
# 3. asyncio.to_thread(...) 把 research_agent(...) 放到背景執行緒，讓研究工作開始跑。
# 4. event_stream() 等 Queue 裡的事件。每拿到一個事件，就用 yield 把它交給 StreamingResponse，再傳給瀏覽器。
# 5. 研究還沒結束時，event_stream() 繼續等下一個事件。等待時不會卡住 event loop。
# 6. 研究結束、Queue 也清空後，event_stream() 取得研究結果，再傳最後一個 complete 事件。

@app.get("/research")
async def research(topic: str):
    # queue = [
    #     {"type": "plan", "message": "Research plan created", "plan": "..."},
    #     {"type": "step", "step": 1, "message": "Agent step 1"},
    #     {"type": "tool", "tool": "search_web", "message": "Using tool: search_web"},
    # ]
    queue = asyncio.Queue()  # 建立一個非同步佇列

    loop = asyncio.get_running_loop()  # 取得目前正在執行的 event loop。這裡是在 FastAPI 的非同步 research() 函式裡取得它

    # 定義一個回呼函式。研究工作每產生一筆進度，就會呼叫它並傳入該筆資料
    # event = {"type": "plan", "message": "Research plan created", "plan": "..."}
    def progress_callback(event):
        # 這行請 event loop 安排執行 queue.put_nowait(event)：把事件放進佇列
        loop.call_soon_threadsafe(queue.put_nowait, event)

    async def event_stream():
        task = asyncio.create_task(
            # research_agent(topic, max_steps=8, progress_callback=progress_callback)
            asyncio.to_thread(research_agent, topic, 8, progress_callback)
        )

        while True:
            # 如果研究工作完成且佇列中沒有更多事件，則跳出循環
            # - task.done()：研究工作是否結束？research_agent 整份工作是否已經結束？
            # - queue.empty()：還有沒有尚未送給瀏覽器的進度 event？
            if task.done() and queue.empty():
                break
            try:
                # 1. 從佇列中取得一個事件，最多等待 0.5 秒，0.5 秒內沒進來：逾時後再開始下一輪等待。
                # event = {
                #     "type": "tool",
                #     "tool": "search_web",
                #     "message": "Using tool: search_web"
                # }
                event = await asyncio.wait_for(queue.get(), timeout=0.5)
                # 2. yield 在這裡的作用是：從 event_stream() 產生一段資料，交給 StreamingResponse 傳給瀏覽器；傳完後，函式暫停在這裡，之後有下一段資料時再繼續。
                # 這讓伺服器可以一段一段傳資料，不用等研究全部完成才一次回傳。
                # * json.dumps(event) 會把 Python 字典轉成 JSON 字串
                # * data: {"type": "tool", "tool": "search_web", "message": "Using tool: search_web"}
                # 研究進度 dict ──json.dumps──> SSE 字串 ──yield──> 瀏覽器
                yield ("data: " + json.dumps(event) + "\n\n")  # 送出一個進度事件

            except asyncio.TimeoutError:
                continue

        # 3. 等待研究工作完成：執行到 result = await task 時，research_agent 已經結束，而且 Queue 裡的進度 event 也已送完。
        result = await task
        # 4. 生成研究完成報告
        # 最後報告 dict ──json.dumps──> SSE 字串 ──yield──> 瀏覽器
        yield ("data: " + json.dumps({"type": "complete", "report": result}) + "\n\n")  # 送出完成事件和報告

    # 它會先把一個「串流回應物件」交給 FastAPI；HTTP 回應開始後，FastAPI 才逐步讀取 event_stream() 產生的內容，並送給瀏覽器。換句話說，research() 函式已經 return，但這個 HTTP 回應還在傳送中。
    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    # 會啟動 Uvicorn 網路伺服器，讓它接收請求並交給 FastAPI 的 app 處理。
    uvicorn.run(app, host="0.0.0.0", port=8001)
