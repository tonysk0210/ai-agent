from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL = "nomic-embed-text-v2-moe"


# 創建嵌入向量的函數 [0.12, -0.34, 0.56, ...]
def create_embedding(text):
    response = client.embeddings.create(
        model=MODEL,
        input=text
    )
    return response.data[0].embedding


# 創建嵌入向量的函數，將文本分割成多個小塊，每個小塊包含指定數量的詞，並且小塊之間有重叠
def embed_chunks(chunks):
    embedded_chunks = []

    for chunk in chunks:
        # 1. 創建嵌入向量
        embedding = create_embedding(chunk["text"])

        # 2. 將小塊文本、來源、小塊編號和嵌入向量添加到嵌入小塊列表中
        embedded_chunks.append({
            "text": chunk["text"],
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "embedding": embedding
        })

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
