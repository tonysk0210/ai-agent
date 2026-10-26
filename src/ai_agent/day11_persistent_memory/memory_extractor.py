import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 擷取記憶
def extract_memory(user_message, assistant_message):
    # 擷取記憶的提示
    prompt = f"""
        你是一個記憶擷取系統。
    
        閱讀以下對話，判斷其中是否包含對使用者有用的長期資訊。
        
        User：
        {user_message}
        
        Assistant：
        {assistant_message}
        
        只有在資訊對未來的對話有幫助時，才儲存該資訊。
        
        有用的資訊包括：
        - 偏好
        - 興趣
        - 目標
        - 技能
        - 專案
        - 重要的使用者個人資訊
        
        請勿儲存：
        - 臨時性問題
        - 目前時間
        - 隨機計算結果
        - 一次性請求
        - 工具執行結果
        - 閒聊內容
        
        如果有有用的資訊，請只回傳應該記住的事實。
        如果沒有值得記住的資訊，請回傳：
        
        NONE
        """

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你負責擷取有用的長期記憶。"
            },

            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
