from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

# MCP Client
from ai_agent.day9_agent_loop.mcp_client import (
    connect,
    disconnect,
    discover_tools
)
from planner import planner
from executor import execute_action  # 執行動作的函數 execute_tool from mcp_client
from loop import run_agent_loop

load_dotenv()

llm = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 格式化答案的函數
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
    response = llm.chat.completions.create(
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
    # 1. 連接到 MCP 伺服器
    client = await connect()

    # 2. 從伺服器取得所有工具
    tools = await discover_tools(client)

    print()
    print("Available Tools")
    print("----------------")

    # 3. 列出所有工具
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
        client
    )

    print()
    print("Final Answer:")

    # 5. 輸出最終答案
    print(state["final_answer"])

    # 6. 斷開與 MCP 伺服器的連線
    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
