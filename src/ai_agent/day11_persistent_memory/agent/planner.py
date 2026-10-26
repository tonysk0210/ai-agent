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

    # 2. 建構提示字串
    prompt = f"""
        你是一個 AI 規劃器。
    
        你的工作是選擇下一個尚未完成的任務，
        並選出最適合完成該任務的工具。
    
        User Request:
        {state["user_request"]}
        
        Relevant Previous Memories:
        {state["memories"]}
        
        Tasks:
        {state["tasks"]}
    
        Pending Tasks:
        {[
        item["task"]
        for item in state["tasks"]
        if item["status"] == "pending"
    ]}
    
        Completed Actions:
        {state["actions"]}
    
        Observations:
        {state["observations"]}
    
        Intermediate Results:
        {state["results"]}
    
        Available Tools:
        {tool_descriptions}
    
        規則：
        1. 只能選擇一個待處理 task。
        2. TASK 必須完全照抄待處理 pending task 中的內容。
        3. 不要更改 task 的文字內容。
        4. 不要選擇已完成的 task。
        5. 為該 task 選擇最合適的可用工具。
        6. 使用先前的 observation，intermediate results 與 relevant previous memories。
        7. 如果動作執行失敗，請重新考慮該 task。
        8. 如果沒有待處理 task，
           只回傳以下這個詞：
        FINISH
        
        9. 如果仍有待處理 task，請嚴格按照以下格式
           回傳兩行：
        TASK: <pending task 原文>
        TOOL: <tool_name>
    
        10. 不要提供任何解釋。
        11. 如果可以直接使用對話記憶或一般知識回答請求，或任務清單為空／NONE，則只能回覆：FINISH
        下一個決策：
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

    # 4. 回傳規劃結果：TASK 與 TOOL 的組合("TASK: 取得目前時間\nTOOL: get_current_time")
    return response.choices[0].message.content.strip()
