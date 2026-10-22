from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 調度工具
def choose_tool(user_request):
    planner_prompt = f"""
    你是一位 AI 規劃助手。
    
    可用工具：
    
    1. get_current_time
       使用時機：使用者詢問目前日期或時間。
    
    2. roll_dice
       使用時機：使用者要求擲骰子。
    
    3. generate_password
       使用時機：使用者需要安全密碼。
    
    如果不需要使用任何工具，請回傳：
    
    none
    
    請只回傳工具名稱。
    
    使用者需求：

    {user_request}
    """

    # 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你是一位 AI 規劃助手。"
            },
            {
                "role": "user",
                "content": planner_prompt
            }
        ]
    )

    # 回傳工具名稱
    return response.choices[0].message.content.strip()
