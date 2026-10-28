import chromadb

# 建立 Chroma DB 用戶端，會在匯入 chroma_store.py 時執行一次
client = chromadb.PersistentClient(path="./chroma_db")

# 取得或創建集合，會在匯入 chroma_store.py 時執行一次
collection = client.get_or_create_collection(name="documents")


# embedded_chunks =
# [
#     {
#         "text": "RAG splits long documents into",
#         "source": "example.txt",
#         "chunk_id": 0,
#         "embedding": [0.12, -0.34, 0.56, ...]
#     },
#     {
#         "text": "documents into chunks for search",
#         "source": "example.txt",
#         "chunk_id": 1,
#         "embedding": [0.08, 0.21, -0.17, ...]
#     }
# ]

# 添加塊，會在呼叫 add_chunks 函數時執行
def add_chunks(embedded_chunks):
    documents = []
    embeddings = []
    ids = []
    metadatas = []

    # 提取塊的文本、嵌入向量、ID 和元數據
    for chunk in embedded_chunks:
        documents.append(chunk["text"])

        embeddings.append(chunk["embedding"])

        # 合併後的字串格式是：example.txt_3
        ids.append(
            f'{chunk["source"]}_'
            f'{chunk["chunk_id"]}'
        )
        # ids = ["example.txt_3"]

        # 填充元數據
        metadatas.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"]
        })
        # metadatas = [
        #     {"source": "example.txt", "chunk_id": 3}
        # ]

    # 將塊添加到集合中 ids、documents、embeddings 和 metadatas 是 Chroma collection.upsert() 接受的參數名稱
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


# 搜尋類似向量
# query_embeddings = [
#     [0.12, -0.34, 0.56]
# ]
def search(query_embedding, top_k=5):
    return collection.query(query_embeddings=[query_embedding], n_results=top_k)
# {
#     "ids": [["example.txt_3", "example.txt_1"]],
#     "documents": [["第三個 chunk 的文字", "第一個 chunk 的文字"]],
#     "metadatas": [[
#         {"source": "example.txt", "chunk_id": 3},
#         {"source": "example.txt", "chunk_id": 1}
#     ]],
#     "distances": [[0.12, 0.28]]
# }
