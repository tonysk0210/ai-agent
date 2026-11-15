from model import model
from prompt import prompt
from langchain_core.output_parsers import StrOutputParser

# StrOutputParser() 建立一個輸出解析器：在這條 chain 中，它把模型回傳的 AIMessage 轉成純文字 str，方便直接列印或繼續處理。
parser = StrOutputParser()

# 1. prompt 用 question 填入 {question}，產生聊天訊息。
# 2. model 接收訊息並回傳 AIMessage。
# 3. parser 從模型回應取出文字，讓 chain.invoke(...) 最後回傳字串給 response。
chain = (prompt | model | parser)

# 呼叫 chain.invoke(...) 並傳入 question，產生回應。
response = chain.invoke(
    {
        "question": "MCP 為什麼對 AI agents 有幫助？"
    }
)

print(response)
