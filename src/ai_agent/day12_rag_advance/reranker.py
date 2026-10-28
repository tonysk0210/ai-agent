from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "qwen3:1.7b"


def rerank(query, hybrid_searched_chunks, top_k=3):
    # 1. 初始化分數列表
    scored = []

    for candidate in hybrid_searched_chunks:

        prompt = f"""
            你是一個文件相關性評估器。
            
            使用者查詢：
            {query}
            
            文件：
            {candidate["text"]}
            
            請給出 0 到 100 的相關性分數。
            
            100 = 直接回答查詢
            0 = 完全不相關
            
            只回傳數字。
            """

        # 2. 呼叫 OpenAI API 生成回應
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        # 3. 取得回應中的分數
        score_text = response.choices[0].message.content.strip()

        try:
            score = float(score_text)
        except ValueError:
            score = 0

        # 4. 將分數加入候選文件
        # **candidate 會把 candidate 字典中的所有鍵和值展開到一個新的字典裡。後面的 "rerank_score": score 再加入 reranker 算出的分數。
        scored.append({**candidate, "rerank_score": score})

    scored.sort(key=lambda item: item["rerank_score"], reverse=True)

    return scored[:top_k]

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
