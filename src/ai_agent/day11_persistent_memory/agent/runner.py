from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio

# MCP Client
from ai_agent.day11_persistent_memory.mcp_client import (
    connect,
    disconnect,
    discover_tools
)
from planner import planner
from executor import execute_action  # 執行動作的函數 execute_tool from mcp_client
from loop import run_agent_loop
from answer import format_answer

load_dotenv()

llm = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


# 定義主函數，接收 Client 物件為參數
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
