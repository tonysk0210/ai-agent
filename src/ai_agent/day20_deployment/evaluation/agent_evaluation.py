from langchain.agents import create_agent

from ..model import model
from mcp_tools import client
from rag_tool import search_knowledge


async def create_agent_instance():
    # 1. 取得 MCP 工具
    mcp_tools = await client.get_tools()
    # 2. 加入知識搜尋工具
    tools = mcp_tools + [search_knowledge]
    # 3. 建立代理
    return create_agent(model=model, tools=tools)
