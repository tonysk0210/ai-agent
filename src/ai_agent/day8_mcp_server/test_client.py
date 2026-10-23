import asyncio  # 用於非同步操作
from mcp_client import *  # 從 mcp_client 模組中引入所有内容


async def main():
    # 1. 連線到 MCP 伺服器
    client = await connect()

    # 2. 從伺服器取得所有工具
    tools = await discover_tools(
        client
    )

    print()
    print("Available Tools")
    print("----------------")

    # 3. 印出所有工具的名稱
    for tool in tools:
        print(tool.name)

    print()

    # 4. 執行工具l
    result = await execute_tool(
        client,
        "roll_dice"
    )

    # 5. 印出骰子結果
    print("Dice Result:", result.content[0].text)

    # 6. 關閉 MCP 連線
    await disconnect(
        client
    )


asyncio.run(main())  # 執行 main 函數
