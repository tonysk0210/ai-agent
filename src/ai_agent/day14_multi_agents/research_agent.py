from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 研究代理
def research(task):
    prompt = f"""
        你是一位研究代理。
        
        你的工作是研究以下任務。
        
        任務：
        {task}
        
        請提供：
        
        1. 重要概念
        2. 關鍵事實
        3. 相關範例
        
        請讓回覆簡潔且實用，
        方便另一個 AI 代理使用。
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

    return response.choices[0].message.content
