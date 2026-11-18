from pydantic import BaseModel


# 這是在用 Pydantic 定義一種名為 ChatRequest 的資料格式：
# • BaseModel 是 Pydantic 提供的基底類別，用來描述並驗證資料。
# • message: str 表示資料必須有一個叫 message 的欄位，而且它應該是字串。
# BaseModel (Pydantic)：就像是一個真實的 Java POJO / DTO 類別 + Bean Validation
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
