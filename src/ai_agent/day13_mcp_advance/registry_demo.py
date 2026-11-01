import asyncio
from mcp_manager import create_tool_registry, close_servers, run_tool


# 主函數
async def main():
    # mcp server 位址清單
    servers = ["time-mcp-server/mcp_server.py", "weather-mcp-server/server.py"]

    # clients = [
    #     <已連線的 FastMCP Client 物件>
    # ]
    #
    # tool_registry = {
    #     "current_time": {...},
    #     "roll_dice": {...},
    #     "generate_password": {...},
    #     "get_weather": {...}
    # }
    clients, tool_registry = (await create_tool_registry(servers))

    try:

        print("\nAvailable Tools")
        print("----------------")

        # 列出所有可用的工具 Python 直接迭代字典時，預設會依序取得鍵 key
        for tool_name in tool_registry:
            print(tool_name)

        # 執行工具
        result = await run_tool(tool_registry, "get_weather", {"city": "Delhi"})

        print("\nTool Result:")
        print(result)
        # result =
        # CallToolResult(
        #     content=[
        #         TextContent(
        #             type='text',
        #             text='Sunny, 32°C',
        #             annotations=None,
        #             meta=None
        #         )
        #     ],
        #     structured_content=None,
        #     data=None,
        #     is_error=False,
        #     meta={
        #         'io.modelcontextprotocol/serverInfo': {
        #             'name': 'Weather Server',
        #             'version': '4.1.3'
        #         }
        #     }
        # )

    finally:
        await close_servers(clients)


if __name__ == "__main__":
    asyncio.run(main())
