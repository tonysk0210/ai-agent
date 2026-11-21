from langchain_core.tools import tool
from retriever import retriever


@tool
def search_knowledge(question: str) -> str:
    """搜尋本機知識庫並回傳相關資訊。"""

    # 1. 取得文件內容
    documents = retriever.invoke(question)
    # documents = [
    #     Document(
    #         page_content="這個 chunk 中與 MCP 相關的文字……",
    #         metadata={"source": "notes.txt"}
    #     ),
    #     # 可能還有其他 Document
    # ]

    # 2. 取出各文件的 page_content，並以兩個換行字元連接
    return "\n\n".join(
        document.page_content
        for document in documents
    )
