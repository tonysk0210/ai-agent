# 分割文本的函數，將文本分割成多個小塊，每個小塊包含指定數量的詞，並且小塊之間有重叠
def create_chunks(text, source, chunk_size=200, overlap=50):
    # 1. 將文本按空格分割成詞列表
    words = text.split()
    # 2. 初始化小塊列表
    chunks = []

    start = 0
    chunk_id = 0

    # 3. 迴圈，直到所有詞都用完為止
    while start < len(words):
        # 4. 計算小塊的結束位置
        end = start + chunk_size  # 200

        # 5. 組合詞列表成小塊文本
        chunk_text = " ".join(words[start:end])

        # 6. 將小塊文本、來源和小塊編號添加到小塊列表中
        chunks.append({
            "text": chunk_text,
            "source": source,
            "chunk_id": chunk_id
        })

        # 7. 更新小塊編號
        chunk_id += 1

        # 8. 更新開始位置
        start += chunk_size - overlap

    return chunks

# chunks =
# [
#     {
#         "text": "RAG splits long documents into",
#         "source": "example.txt",
#         "chunk_id": 0
#     },
#     {
#         "text": "documents into chunks for search",
#         "source": "example.txt",
#         "chunk_id": 1
#     },
#     {
#         "text": "for search and retrieval",
#         "source": "example.txt",
#         "chunk_id": 2
#     }
# ]
