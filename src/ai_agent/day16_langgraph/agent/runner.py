from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

llm = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 格式化答案的函數
def format_answer(state):
    # 1. 建立提示字串，包含使用者問題、已執行的動作(非必要) 和執行結果
    prompt = f"""
    使用者提出的問題：
        {state["user_request"]}

    已執行的動作：
        {state["actions"]}

    執行結果：
        {state["observations"]}

    請自然地回答使用者。

    不要提及內部規劃。
    不要提及狀態。
    不要提及工具。
    """

    # 2. 呼叫 OpenAI API 生成回應
    response = llm.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
