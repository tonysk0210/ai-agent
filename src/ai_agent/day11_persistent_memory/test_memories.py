from memory import (
    create_database,
    save_memory,
    search_semantic_memories
)

create_database()

save_memory(
    "我叫 Anthony。",
    "很高興認識你，Anthony。"
)

save_memory(
    "我正在學習 Python。",
    "Python 對 AI 開發很有幫助。"
)

save_memory(
    "我正在學習 MCP。",
    "MCP 讓 AI 應用程式能夠使用工具。"
)

# 搜尋語義類似的記憶
results = search_semantic_memories(
    "What is my name"
)

print("\nRelevant Memories")
print("-----------------")

# 印出相關的記憶
for result in results:
    print("\nScore:", result["score"])
    print("User:", result["user_message"])
    print("Assistant:", result["assistant_message"])
