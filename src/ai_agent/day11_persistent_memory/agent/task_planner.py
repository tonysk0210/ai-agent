import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 任務拆解
def decompose_task(user_request):
    prompt = f"""
        你是一個 AI 任務規劃器。
        
        將使用者的需求拆解成較小的任務。
        
        規則：
        1. 只建立必要的任務。
        2. 按照執行順序排列任務。
        3. 每個任務都應該是一個簡短的動作。
        4. 每行回傳一個任務。
        5. 不要為任務加上編號。
        6. 不要提供任何解釋。
        
        重要規則：
        如果使用者的需求屬於以下任一類別，請不要建立任何任務（或回傳「NONE」）：
           1. 問候或閒聊（例如：「嗨」、「你好」、「你好嗎？」）
           2. 自我介紹或個人資訊（例如：「我叫 Anthony」、「我住在台北」）
           3. 關於過去對話的記憶問題（例如：「我叫什麼名字？」、「我們之前聊了什麼？」）
           4. 不使用工具即可直接回答的一般知識或問答（例如：「什麼是機器學習？」、「請解釋重力」）
        
        使用者需求：
        {user_request}
        """

    # 呼叫 OpenAI API
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你是一個 AI 任務規劃器。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 解析回應
    result = response.choices[0].message.content.strip()

    # 將回應拆分成任務
    tasks = []
    for line in result.splitlines():
        line = line.strip()
        if line:
            tasks.append(line)

    return tasks
