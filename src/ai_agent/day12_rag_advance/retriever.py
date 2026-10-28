import numpy as np
from embeddings import create_embedding


# 計算向量餘弦相似度的函數
def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# 協同搜索函數
def semantic_search(query, embedded_chunks, top_k=5):
    # 1. 產生 query 的 embedding 向量值 [0.12, -0.34, 0.56, ...]
    query_embedding = create_embedding(query)

    results = []

    # 2. 計算 query 與每個小塊的餘弦相似度
    for chunk in embedded_chunks:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        # 3. 將小塊的文本、來源、編號和相似度分數加入結果列表
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "semantic_score": score
        })

    # 排序時，對每個 item 取出它的 semantic_score 當作排序依據。
    # • key=：sort() 的參數，指定用什麼值來比較列表中的元素。
    # • lambda item:：建立一個簡短函式，接收一個叫 item 的值。
    # • item["semantic_score"]：函式回傳該字典裡的相似度分數。
    results.sort(key=lambda item: item["semantic_score"], reverse=True)

    return results[:top_k]


# results =
# [
#     {
#         "text": "這個 chunk 的文字內容",
#         "source": "example.txt",
#         "chunk_id": 0,
#         "semantic_score": 0.87
#     },
#     {
#         "text": "另一個 chunk 的文字內容",
#         "source": "example.txt",
#         "chunk_id": 2,
#         "semantic_score": 0.73
#     }
# ]

# 關鍵字分數計算函數
def keyword_score(query, text):
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())

    # 1. 如果查詢詞集合為空，返回 0.0
    if not query_words:
        return 0.0

    # 2. 計算查詢詞和文本詞的交集
    matches = (query_words & text_words)

    # 3. 計算關鍵字分數
    return len(matches) / len(query_words)


# keyword_score(
#     "python AI",
#     "Python helps build AI apps"
# )
# # 1.0


# 混合搜索函數
def hybrid_search(
        query,
        embedded_chunks,
        top_k=5,
        semantic_weight=0.7,
        keyword_weight=0.3
):
    # 1. 產生 query 的 embedding 向量值 [0.12, -0.34, 0.56, ...]
    query_embedding = create_embedding(query)

    # 2. 初始化結果列表
    results = []

    # 3. 計算每個小塊的語義分數和關鍵字分數
    for chunk in embedded_chunks:
        semantic = cosine_similarity(query_embedding, chunk["embedding"])

        # 4. 計算每個小塊的關鍵字分數
        keyword = keyword_score(query, chunk["text"])

        # 5. 計算每個小塊的混合分數
        combined = (semantic * semantic_weight + keyword * keyword_weight)

        # 6. 將小塊的文本、來源、編號和分數加入結果列表
        results.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "semantic_score": semantic,
            "keyword_score": keyword,
            "combined_score": combined
        })

    results.sort(key=lambda item: item["combined_score"], reverse=True)

    return results[:top_k]
# [
#     {
#         "text": "chunk 的文字內容",
#         "source": "example.txt",
#         "chunk_id": 0,
#         "semantic_score": 0.80,
#         "keyword_score": 0.50,
#         "combined_score": 0.71
#     }
# ]
