from retriever import retriever

results = retriever.invoke("What is MCP?")
# results = [
#     Document(
#         page_content="這個 chunk 中與 MCP 相關的文字……",
#         metadata={"source": "notes.txt"}
#     ),
#     # 可能還有其他 Document
# ]

for document in results:
    print("\n--- DOCUMENT ---")
    print(document.page_content)
