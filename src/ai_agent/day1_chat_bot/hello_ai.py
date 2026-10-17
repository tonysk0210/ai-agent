import os  # 用於載入環境變數
from dotenv import load_dotenv  # 用於載入環境變數
from openai import OpenAI  # 用於與 OpenAI API 進行互動

load_dotenv()  # 載入環境變數

# 1. 建立一個客戶端，用於與 Ollama 進行通訊
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# 2. 向 AI 模型提出問題
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "什麼是人工智慧？"
        }
    ]
)

# 3. 輸出 AI 模型的回答
print(response.choices[0].message.content)
