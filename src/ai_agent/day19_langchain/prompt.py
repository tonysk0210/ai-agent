from langchain_core.prompts import ChatPromptTemplate

# 建立對話模板，定義了對話的系統角色和使用者輸入
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一位 AI agent 工程講師。"
        ),
        (
            "human",
            "{question}"
        )
    ]
)

