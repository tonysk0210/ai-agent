from pydantic import BaseModel


# 定義研究請求的資料格式
class ChatRequest(BaseModel):
    message: str


# 定義研究回應的資料格式
class ChatResponse(BaseModel):
    response: str
