from fastapi import FastAPI, HTTPException

from schemas import ChatRequest, ChatResponse  # 輸入的資料格式

from agent import agent

# 這行建立一個 FastAPI 應用程式物件，並把它指定給 app。同一個檔案接著用 app.post("/chat") 在這個應用程式上註冊 /chat 路由。
app = FastAPI(title="AI Agent API", version="1.0.0")


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
