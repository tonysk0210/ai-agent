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

msgs = []  # 用於儲存對話消息

# 1. 迴圈，等待用戶輸入
while True:
    user_input = input("\nYou : ")

    # 2. 將用戶輸入添加到對話消息中
    msgs.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    if user_input.lower() == "quit":
        print("\nAI  : 再見！祝你今天愉快。")
        break

    # 3. 向 AI 模型提出問題
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=msgs
    )

    ai_reply = response.choices[0].message.content  # 取得 AI 的回答

    # 3. 輸出 AI 模型的回答
    print("\nAI :", ai_reply)

    # 4. 將 AI 的回答添加到對話消息中
    msgs.append(
        {
            "role": "assistant",
            "content": ai_reply
        }
    )

    # 5. 輸出對話歷史
    print("\n---------- Conversation History ----------")
    for msg in msgs:
        print(msg)
    print("------------------------------------------")
