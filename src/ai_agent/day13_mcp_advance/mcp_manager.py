from mcp_client import connect, disconnect, discover_tools, execute_tool


# 建立工具註冊表；servers 是一個包含多個伺服器位址的清單 list
async def create_tool_registry(servers):
    clients = []
    tool_registry = {}

    # 建立工具註冊表
    for server in servers:

        client = await connect(server)
        clients.append(client)
        tools = await discover_tools(client)

        for tool in tools:
            # 將工具加入註冊表
            tool_registry[tool.name] = {
                "client": client,
                "tool": tool
            }

    return clients, tool_registry


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

# 關閉所有伺服器連線
async def close_servers(clients):
    for client in clients:
        await disconnect(client)


# 執行工具
# tool_registry = {
#     "get_weather": {
#         "client": <提供 get_weather 的 Client 物件>,
#         "tool": <FastMCP Tool 物件>
#     }
# }
async def run_tool(tool_registry, tool_name, arguments):
    # 從註冊表中取得工具
    entry = tool_registry.get(tool_name)
    # entry = {
    #     "client": <提供 get_weather 的 FastMCP Client 物件>,
    #     "tool": <get_weather 的 FastMCP Tool 物件>
    # }

    if entry is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    # 執行工具
    return await execute_tool(entry["client"], tool_name, arguments)
