from pydantic import BaseModel


# 定義研究請求的資料格式
class ResearchRequest(BaseModel):
    topic: str


# 定義研究回應的資料格式
class ResearchResponse(BaseModel):
    report: str
