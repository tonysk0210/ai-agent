import json
import sqlite3
import numpy as np
from openai import OpenAI

# 資料庫名稱
DATABASE = "memory.db"

# 嵌入模型客戶端
embedding_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# 創建資料庫
def create_database():
    connection = sqlite3.connect(DATABASE)  # 連接到資料庫
    cursor = connection.cursor()  # 創建游標物件

    # 創建 memories 表格
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories
        (
            id
            INTEGER
            PRIMARY
            KEY
            AUTOINCREMENT,
            user_message
            TEXT,
            assistant_message
            TEXT,
            embedding
            TEXT,
            created_at
            TIMESTAMP
            DEFAULT
            CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()  # 提交變更
    connection.close()  # 關閉連接


# 產生 embedding 向量值
def create_embedding(text):
    # 調用嵌入模型 API
    response = embedding_client.embeddings.create(
        model="nomic-embed-text-v2-moe",
        input=text
    )

    # 回傳嵌入向量
    return response.data[0].embedding


# 計算向量餘弦相似度
def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)
    v2 = np.array(vector2)

    return np.dot(v1, v2) / (
            np.linalg.norm(v1) *
            np.linalg.norm(v2)
    )


# 儲存記憶
def save_memory(user_message, assistant_message):
    # 1. 將用戶和助理的對話合併成一塊文本
    text = user_message + "\n" + assistant_message

    # 2. 產生 embedding 向量值
    embedding = create_embedding(text)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # 3. 將對話和 embedding 向量值儲存到資料庫
    cursor.execute(
        """
        INSERT INTO memories
        (user_message,
         assistant_message,
         embedding)
        VALUES (?, ?, ?)
        """,
        (
            user_message,
            assistant_message,
            json.dumps(embedding)  # 嵌入向量轉換為 JSON 字串
        )
    )

    connection.commit()
    connection.close()


# 搜尋語義類似的記憶
def search_semantic_memories(
        query,
        top_k=3,
        threshold=0.20
):
    # 1. 產生 query 的 embedding 向量值
    query_embedding = create_embedding(query)

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
                   SELECT user_message,
                          assistant_message,
                          embedding,
                          created_at
                   FROM memories
                   """)

    # 2. 讀取資料庫中的所有記憶
    rows = cursor.fetchall()

    connection.close()

    # 3. 計算 query 與每個記憶的餘弦相似度
    results = []

    for (user_message, assistant_message, embedding_json, created_at) in rows:

        # 4. 將 embedding 向量值從 JSON 字串轉換為 Python 列表
        memory_embedding = json.loads(embedding_json)

        # 5. 計算 query 與記憶的餘弦相似度
        score = cosine_similarity(query_embedding, memory_embedding)
        print(f"Score: {score:.4f}")

        # 6. 檢查相似度是否大於閾值 0.20
        if score >= threshold:
            # 7. 將相似度大於閾值的記憶加入結果列表
            results.append({
                "user_message": user_message,
                "assistant_message": assistant_message,
                "created_at": created_at,
                "score": score
            })

    # 8. 將結果列表依相似度由高到低排序
    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )
    print(f"Results: {len(results)}")

    # print(results)
    # 9. 回傳相似度最高的前 top_k 個記憶
    # : 在這裡是 Python 的**切片（slice）**語法。就等同於：results[0:3]
    # 會取出索引 0、1、2 的項目，也就是最多前三筆。若 results 不足三筆，則會回傳現有的全部項目。
    return results[:top_k]
