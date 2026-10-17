import os  # 用於載入環境變數
from dotenv import load_dotenv  # 用於載入環境變數
from openai import OpenAI  # 用於與 OpenAI API 進行互動

load_dotenv()  # 載入環境變數
# 建立一個客戶端，用於與 Ollama 進行通訊
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# 1. 迴圈，等待用戶輸入
while True:
    user_input = input("\nYou : ")
    if user_input.lower() == "quit":
        print("\nAI  : 再見！祝你今天愉快。")
        break

    # 2. 向 AI 模型提出問題
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    # 3. 輸出 AI 模型的回答
    print("\nAI :", response.choices[0].message.content)
