from chunker import create_chunks  # 創建塊
from embeddings import embed_chunks, create_embedding  # 創建嵌入向量
from chroma_store import add_chunks, search as chroma_search  # 添加塊，搜尋類似向量
from retriever import keyword_score  # 關鍵字分數
from reranker import rerank  # 重新排序


# 建立 RAG
def build_rag(text, source):
    # 1. 創建塊
    chunks = create_chunks(text, source, chunk_size=200, overlap=50)

    # 2. 創建嵌入向量
    embedded_chunks = embed_chunks(chunks)

    # 3. 添加塊
    add_chunks(embedded_chunks)

    return embedded_chunks


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

# 搜尋類似向量
def retrieve(query, top_k=5):
    # 1. 創建查詢嵌入向量 [0.12, -0.34, 0.56, ...]
    query_embedding = create_embedding(query)

    # 2. 搜尋類似向量
    # {
    #     "ids": [["example.txt_3", "example.txt_1"]],
    #     "documents": [["第三個 chunk 的文字", "第一個 chunk 的文字"]],
    #     "metadatas": [[
    #         {"source": "example.txt", "chunk_id": 3},
    #         {"source": "example.txt", "chunk_id": 1}
    #     ]],
    #     "distances": [[0.12, 0.28]]
    # }
    semantic_results = chroma_search(query_embedding, top_k=top_k)

    candidates = []

    documents = (semantic_results["documents"][0])  # ["第三個 chunk 的文字", "第一個 chunk 的文字"]

    metadatas = (semantic_results["metadatas"][0])  # [{"source": "example.txt", "chunk_id": 3},　{"source": "example.txt", "chunk_id": 1}]

    distances = (semantic_results["distances"][0])  # [0.12, 0.28]

    for i in range(len(documents)):
        text = documents[i]

        metadata = metadatas[i]

        distance = distances[i]

        semantic = 1 / (1 + distance)

        # 計算關鍵字分數
        keyword = keyword_score(query, text)

        combined = (0.7 * semantic + 0.3 * keyword)

        candidates.append({
            "text": text,
            "source": metadata["source"],
            "chunk_id": metadata["chunk_id"],
            "semantic_score": semantic,
            "keyword_score": keyword,
            "combined_score": combined
        })

    candidates.sort(key=lambda item: item["combined_score"], reverse=True)
    candidates = candidates[:top_k]
    # candidates =
    # [
    #     {
    #         "text": "chunk 的文字內容",
    #         "source": "example.txt",
    #         "chunk_id": 3,
    #         "semantic_score": 0.893,
    #         "keyword_score": 0.50,
    #         "combined_score": 0.775
    #     },
    #     ...
    # ]

    print("\nRetrieved Sources Candidates:")

    for candidate in candidates:
        print(
            f"- "
            f"{candidate['source']} "
            f"(chunk "
            f"{candidate['chunk_id']})"
        )

    return rerank(query, candidates, top_k=3)
    # 根據 llm 重新排序（0 到 100 的相關性分數），返回前 3 個　請給出
    # [
    #     {
    #         "text": "第一段 chunk 的文字",
    #         "source": "example.txt",
    #         "chunk_id": 0,
    #         "semantic_score": 0.80,
    #         "keyword_score": 0.50,
    #         "combined_score": 0.71,
    #         "rerank_score": 92.0
    #     },
    #     {
    #         "text": "第二段 chunk 的文字",
    #         "source": "example.txt",
    #         "chunk_id": 1,
    #         "semantic_score": 0.75,
    #         "keyword_score": 0.30,
    #         "combined_score": 0.62,
    #         "rerank_score": 75.0
    #     }
    # ]
