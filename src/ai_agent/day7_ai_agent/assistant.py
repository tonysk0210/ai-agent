from openai import OpenAI
from dotenv import load_dotenv
import os

from planner import choose_tool
from tools import (
    get_current_time,
    roll_dice,
    generate_password
)

# 載入環境變數
load_dotenv()
# 創建 AI 客戶端
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

# 1. 無限循環，等待用戶輸入
while True:
    user_input = input("\nYou : ")
    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    # 2. 選擇工具
    tool = choose_tool(user_input)
    print(f"Tool chosen: {tool}")

    # 3. 呼叫工具函數
    if tool == "get_current_time":
        result = get_current_time()
    elif tool == "roll_dice":
        result = roll_dice()
    elif tool == "generate_password":
        result = generate_password()
    else:
        result = None

    # 4. 建立提示詞 - 使用者提出的問題及工具回傳的結果
    prompt = f"""
    使用者提出的問題：
    {user_input}
    工具回傳的結果：
    {result}
    請自然地回答使用者，不要自行補充其他內容。如果工具回傳 none，請由語言模型直接回答。
    """

    # 5. 呼叫 OpenAI API 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 6. 輸出回應
    print("\nAI :", response.choices[0].message.content)
