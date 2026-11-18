from fastapi import FastAPI
from pydantic import BaseModel

from agent import agent

# 這行建立一個 FastAPI 應用程式物件，並把它指定給 app。同一個檔案接著用 app.post("/chat") 在這個應用程式上註冊 /chat 路由。
app = FastAPI(title="AI Agent API", version="1.0.0")


# 這是在用 Pydantic 定義一種名為 ChatRequest 的資料格式：
# • BaseModel 是 Pydantic 提供的基底類別，用來描述並驗證資料。
# • message: str 表示資料必須有一個叫 message 的欄位，而且它應該是字串。
# BaseModel (Pydantic)：就像是一個真實的 Java POJO / DTO 類別 + Bean Validation
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message # 輸入的訊息 Pydantic 驗證發生在此時！
                }
            ]
        }
    )

    return {
        "answer": result["messages"][-1].content
    }
