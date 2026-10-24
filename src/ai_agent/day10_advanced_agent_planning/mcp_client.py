from fastmcp import Client  # 連線到某個已存在的 MCP 伺服器，主動向它索取工具清單，並觸發執行那些工具。
from pathlib import Path


# 連線到 MCP 伺服器
async def connect():
    """連線到 MCP 伺服器。"""
    client = Client(Path(__file__).with_name("mcp_server.py"))  # 建立一個 Client 物件，指定要連線的 MCP 伺服器。此時尚未進入連線階段。
    await client.__aenter__()  # 手動進入 Client 的非同步 context，建立連線並初始化通訊。await 是因為連線操作需要非同步執行
    print("Connected to MCP Server.")
    return client


# 關閉 MCP 連線
async def disconnect(client):
    """關閉 MCP 連線。"""
    await client.__aexit__(None, None, None)  # 關閉 MCP 連線


# 從伺服器取得所有工具
async def discover_tools(client):
    """從伺服器取得所有工具。"""
    tools = await client.list_tools()  # 從伺服器取得所有工具
    return tools


# 執行工具; arguments 是工具的參數：預設為 None，結構為 dict
async def execute_tool(client, tool_name, arguments=None):
    """執行工具。"""
    if arguments is None:
        arguments = {}

    # await client.call_tool("generate_password", {"length": 12})
    result = await client.call_tool(tool_name, arguments)  # 執行工具
    return result
