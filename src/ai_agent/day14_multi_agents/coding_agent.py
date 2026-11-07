from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 程式撰寫代理
def write_code(task, research, feedback=""):
    prompt = f"""
        你是一位程式撰寫代理。
        
        請根據任務與研究資料撰寫 Python 程式碼。
        
        任務：
        {task}
        
        研究資料：
        {research}
        
        審查者先前的回饋：
        {feedback}  
        
        如果有提供審查者的回饋，請修正其中指出的問題。
        
        請提供：
            1. 簡短說明
            2. 完整的 Python 程式碼
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
