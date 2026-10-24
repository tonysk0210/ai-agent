import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 格式化答案的函數
def format_answer(state):
    # 1. 建立提示字串，包含使用者問題、任務清單、已執行的動作、觀察和中間結果
    prompt = f"""
        使用者問題:
        {state["user_request"]}
        
        Tasks:
        {state["tasks"]}
        
        Actions:
        {state["actions"]}
        
        Observations:
        {state["observations"]}
        
        Intermediate Results:
        {state["results"]}
        
        請自然且簡潔地回答使用者。
        
        請勿提及：
        - planner
        - agent loop
        - MCP
        - 內部狀態
        - 工具
        - 內部推理
        """

    # 2. 呼叫 OpenAI API 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
