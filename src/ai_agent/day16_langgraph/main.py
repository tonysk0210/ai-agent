import asyncio

from agent.mcp_client import connect, disconnect, discover_tools
from graph import build_graph


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

    # 4. 建立 LangGraph
    graph = build_graph(tools)

    user_request = input("\nUser : ")

    # 5. 建立 state 初始狀態
    initial_state = {
        "user_request": user_request,
        "current_step": 0,
        "max_steps": 5,
        "actions": [],
        "observations": [],
        "finished": False,
        "final_answer": ""
    }

    # 6. 呼叫 LangGraph 並傳入初始狀態，並回傳最終狀態
    result_state = graph.invoke(initial_state)

    print("\nFinal State")
    print("-----------")
    print(result_state)  # 印出最終狀態

    await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
