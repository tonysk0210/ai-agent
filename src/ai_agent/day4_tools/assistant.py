import os  # 用於載入環境變數
from dotenv import load_dotenv  # 用於載入環境變數
from openai import OpenAI  # 用於與 OpenAI API 進行互動

from tool_manager import execute_tool  # 加入工具管理器

load_dotenv()  # 載入環境變數
# 建立一個客戶端，用於與 Ollama 進行通訊
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# 定義不同角色的描述
roles = {
    "1": "你是一位親切的學校老師。請用簡單的語言和生活中的實例，解釋每個概念。",

    "2": "你是一位資深的 Python 開發者。請清楚解釋程式設計概念，並務必附上 Python 範例。",

    "3": "你是一位經驗豐富的旅遊導覽員。請推薦景點、美食、交通方式和旅遊須知。",

    "4": "你是一位激勵人心的教練。請以正向的態度鼓勵使用者，並提供實用建議。",

    "5": "你是一位專業的面試官。請一次提出一個面試問題，並在每次回答後提供回饋。"
}

print("\n選擇你的 AI 助理\n")

print("1. 老師")
print("2. Python 專家")
print("3. 旅遊導覽員")
print("4. 激勵教練")
print("5. 面試官")

choice = input("\nEnter your choice : ")  # 輸入選擇

# 用於儲存對話消息
msgs = [
    {
        "role": "system",
        "content": roles.get(choice, "你是一位樂於助人的 AI 助理。")  # 根據選擇提供不同的角色描述
    }
]

# 1. 迴圈，等待用戶輸入
while True:
    user_input = input("\nYou : ")

    tool_result = execute_tool(user_input)  # 執行工具函數

    # 如果工具函數有回傳值，則輸出工具函數的回傳值
    if tool_result:
        print("\nAI :", tool_result)
        continue

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
