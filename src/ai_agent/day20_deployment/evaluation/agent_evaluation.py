from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from mcp_tools import client
from rag_tool import search_knowledge

model = ChatOllama(model="qwen3:1.7b")

async def create_agent_instance():
    # 1. 取得 MCP 工具
    mcp_tools = await client.get_tools()
    # 2. 加入知識搜尋工具
    tools = mcp_tools + [search_knowledge]
    # 3. 建立代理
    return create_agent(model=model, tools=tools)
