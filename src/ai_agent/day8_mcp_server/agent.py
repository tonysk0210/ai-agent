from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import os

# 從 mcp_client 模組中引入需要的函數
from mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool
)

# 載入環境變數
load_dotenv()

# 創建 AI 用戶端
llm = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 動態建立工具描述
# Tool:
# current_time
#
# Description:
# 回傳目前的日期和時間。
# ----------------------------
#
# Tool:
# roll_dice
#
# Description:
# 擲一顆六面骰子。
# ----------------------------
#
# Tool:
# generate_password
#
# Description:
# 產生安全的密碼。
# ----------------------------
def build_tool_descriptions(tools):
    descriptions = ""
    # 迭代所有工具並建立描述
    for tool in tools:
        descriptions += f"""
        Tool:
        {tool.name}
        
        Description:
        {tool.description}
        ----------------------------
        """
    return descriptions


# 計畫師函數，根據用戶請求選擇最適合的工具
def planner(user_request, tools):
    # 1. 動態建立工具描述
    tool_descriptions = build_tool_descriptions(tools)

    ### 將使用者輸入和工具描述組合成提示，然後將提示傳給 Ollama。 ###
    prompt = f"""
        你是一位 AI 規劃助手。
        
        可用工具
        
        {tool_descriptions}
        
        指示
        
        1. 選擇最適合的工具。
        2. 只回覆工具名稱。
        3. 不要解釋。
        
        使用者需求
        
        {user_request}
        """
    # 將此提示傳給 Ollama
    response = llm.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Ollama 回傳工具名稱
    tool_name = response.choices[0].message.content

    return tool_name.strip()


# 生成回應函數，根據工具名稱執行相應的工具
def generate_response(user_request, tool_result):
    # 建立提示
    prompt = f"""
    使用者提出的問題：
    {user_request}
    
    工具回傳的結果：
    {tool_result}
    
    請以自然、像對話般的方式直接回答使用者。
    
    以工具回傳的結果作為事實依據。
    將工具的原始輸出整理成容易理解的回答。
    如果用自然的句子表達更好，就不要只是照抄原始值。
    不要加入回答問題不需要的資訊。
    不要提及工具、內部處理流程、規劃或推理。
    回答請保持簡潔。
    """

    # 將此提示傳給 Ollama
    response = llm.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # 將 Ollama 的回應傳給用戶
    return response.choices[0].message.content


# 定義 main 函數
async def main():
    # 1. 連線到 MCP 伺服器
    client = await connect()

    # 2. 從伺服器取得所有工具
    tools = await discover_tools(
        client
    )

    print("可用工具")
    print("----------------")

    # 3. 印出所有工具的名稱
    for tool in tools:
        print(tool.name)
    print()

    # 4. 從用戶那裡取得輸入
    user_request = input(
        "User : "
    )

    # 5. 根據用戶輸入選擇最適合的工具
    selected_tool_name = planner(user_request, tools)

    print()
    print("Planner Selected:", selected_tool_name)  # 輸出 Planner 選擇的工具

    # 6. 執行所選工具
    tool_result = await execute_tool(client, selected_tool_name)

    # 7. 生成自然語言回應
    final_answer = generate_response(user_request, tool_result)

    print()
    print(final_answer)

    # 8. 關閉 MCP 連線
    await disconnect(
        client
    )


if __name__ == "__main__":
    asyncio.run(main())
