from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 建構工具描述字串函數
def build_tool_descriptions(tools):
    descriptions = ""
    # 迭代所有工具並建立描述
    for tool in tools:
        descriptions += f"""
            Tool：
            {tool.name}
            Description：
            {tool.description}
            ----------------------------
            """
    return descriptions


# 規劃函數，根據當前狀態和工具列表回傳下一步動作
def planner(state, tools):
    # 1. 建構工具描述字串
    tool_descriptions = build_tool_descriptions(tools)

    # 2. 建構提示：含使用者需求、已完成動作、先前觀察、工具描述及規則
    prompt = f"""
        你是一位 AI 規劃助手。
        
        你的工作是只決定下一個動作。
        
        使用者需求：
        {state["user_request"]}
        
        已完成的動作：
        {state["actions"]}
        
        先前的觀察結果：
        {state["observations"]}
        
        可用工具：
        {tool_descriptions}
        
        規則：
        
        1. 只選擇一個下一步動作。
        2. 不要重複已經完成的動作。
        3. 根據觀察結果判斷還需要完成哪些事項。
        4. 如果使用者的需求已全部完成，請回傳 FINISH。
        5. 只回傳工具名稱或 FINISH。
        6. 不要解釋你的答案。
        
        下一步動作：
        """

    # 3. 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你是一位 AI 規劃助手。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 4. 回傳工具名稱
    return response.choices[0].message.content.strip()
