from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

from mcp_manager import create_tool_registry, close_servers
from planner import planner
from executor import execute_action  # 執行動作的函數
from loop import run_agent_loop

servers = ["time-mcp-server/mcp_server.py", "weather-mcp-server/server.py"]

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 格式化答案
def format_answer(state):
    # 1. 建立提示字串，包含使用者問題、已執行的動作(非必要) 和執行結果
    prompt = f"""
    使用者提出的問題：
        {state["user_request"]}

    已執行的動作：
        {state["actions"]}

    執行結果：
        {state["observations"]}

    請自然地回答使用者。

    不要提及內部規劃。
    不要提及狀態。
    不要提及工具。
    """

    # 2. 呼叫 OpenAI API 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


async def main():
    # 1. 創建工具註冊表和客戶端清單
    # clients = [
    #     <已連線的 FastMCP Client 物件>
    # ]
    #
    # tool_registry = {
    #     "get_weather": {
    #         "client": <提供 get_weather 的 Client 物件>,
    #         "tool": <FastMCP Tool 物件>
    #     }
    # }
    clients, tool_registry = await create_tool_registry(servers)

    # 2. 從工具註冊表中提取工具清單
    tools = [entry["tool"] for entry in tool_registry.values()]

    # 3. 列出所有工具
    print()
    print("Available Tools")
    print("----------------")
    for tool in tools:
        print(tool.name)

    user_request = input("\nUser : ")

    # 4. 執行 agent loop
    state = await run_agent_loop(
        user_request,
        planner,
        execute_action,
        format_answer,
        tools,
        tool_registry
    )

    # 5. 輸出最終答案
    print()
    print("Final Answer:")
    print(state["final_answer"])

    # 6. 關閉所有伺服器
    await close_servers(clients)


if __name__ == "__main__":
    asyncio.run(main())
