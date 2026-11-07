from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 程式碼審查代理
def review(task, code):
    prompt = f"""
        你是一位程式碼審查代理。
        
        請審查以下解答。
        
        任務：
        {task}
        
        解答：
        {code}
        
        請檢查：
        
        1. 正確性
        2. Python 語法
        3. 邏輯
        4. 遺漏的問題
        5. 可行的改進
        
        只回傳有效的 JSON。

        請嚴格使用以下格式：
        
        {{
            "status": "approved",
            "feedback": "解答正確。"
        }}
        
        或：
        
        {{
            "status": "needs_revision",
            "feedback": "說明需要修改的地方。"
        }}
        
        只有在解答可接受時，才使用 "approved"。

        解答需要修正時，請使用 "needs_revision"。
        """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    return json.loads(result)  # 轉換為 JSON 格式
    #         {{
    #             "status": "approved",
    #             "feedback": "解答正確。"
    #         }}
    #
    #         或：
    #
    #         {{
    #             "status": "needs_revision",
    #             "feedback": "說明需要修改的地方。"
    #         }}
