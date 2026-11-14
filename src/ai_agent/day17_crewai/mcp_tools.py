import asyncio

from crewai.tools import tool  # 這是 crewai 的工具模組
from mcp_client import connect, execute_tool, disconnect


async def call_mcp_current_time():
    client = await connect()

    try:
        # 1. 呼叫 MCP 的 current_time 工具
        result = await execute_tool(client, "current_time")
        # 2. 回傳結果
        return result.content[0].text
    finally:
        await disconnect(client)


@tool("MCP Current Time")
def mcp_current_time() -> str:
    """從 MCP 取得目前的日期與時間。"""
    return asyncio.run(call_mcp_current_time())
