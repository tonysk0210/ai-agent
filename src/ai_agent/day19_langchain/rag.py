from model import model
from retriever import retriever

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 建立提示模板
prompt = ChatPromptTemplate.from_template(
    """
    請只根據提供的上下文回答問題。
    
    上下文：
    {context}
    
    問題：
    {question}
    """
)


# 2. 建立上下文取得函數
def get_context(question):
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


chain = (
    # 對 ChatPromptTemplate 來說，呼叫 prompt.invoke(...) 時要提供一組輸入值，通常用 dictionary，而且 key 要對應模板中的變數名稱
        {
            "context": get_context,
            "question": lambda x: x  # 回傳 "What is MCP?"
        }
        | prompt
        | model
        | StrOutputParser()
)
# lambda x: x
#        │  └── 回傳 x
#        └───── 接收名為 x 的輸入

# 相當於
# def keep_question(x):
#     return x
#
# chain = (
#         {
#             "context": get_context,
#             "question": keep_question
#         }
#         | prompt
#         | model
#         | StrOutputParser()

answer = chain.invoke("What is MCP?")

print(answer)
