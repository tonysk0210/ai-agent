import asyncio

from langchain.agents import create_agent
from langchain_core.tools import tool

from model import model
from mcp_tools import client
from retriever import retriever


@tool
def search_knowledge(question: str) -> str:
    """搜尋本機知識庫並回傳相關資訊。"""

    documents = retriever.invoke(question)
    # documents = [
    #     Document(
    #         page_content="第一段切分後的文字……",
    #         metadata={"source": "notes.txt"}
    #     ),
    #     Document(
    #         page_content="第二段切分後的文字……",
    #         metadata={"source": "notes.txt"}
    #     ),
    # ]

    return "\n\n".join(
        document.page_content
        for document in documents
    )


async def main():
    # 1. 建立检索器 - 建立向量存儲的檢索器
    mcp_tools = await client.get_tools()
    # current_time
    # roll_dice
    # generate_password

    # 2. 建立工具清單 - 搬家工具清單
    tools = mcp_tools + [search_knowledge]

    agent = create_agent(model=model, tools=tools)

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "According to my notes, what is MCP?"
                }
            ]
        }
    )

    print("\nFINAL ANSWER")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
