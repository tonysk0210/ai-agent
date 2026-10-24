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
