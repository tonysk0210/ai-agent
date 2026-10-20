from openai import OpenAI
from dotenv import load_dotenv
import os

from retriever import load_documents
from test_embedding import create_embedding
from similarity import cosine_similarity

load_dotenv()

# 1. 建立 filename 和 content
documents = load_documents()
# documents = {
#     "python.txt": "Python 是一種程式語言……",
#     "ai.txt": "人工智慧是……"
# }

print("Loading documents...", documents)

# 2. 建立文件名稱和嵌入向量的映射
document_embeddings = {}
for filename, content in documents.items():
    document_embeddings[filename] = create_embedding(
        content
    )
# document_embeddings = {
#     "python.txt": [0.012, -0.034, 0.056, ...],
#     "ai.txt":     [-0.021, 0.043, 0.078, ...]
# }

# 3. 建立 OpenAI 客戶端
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print("=" * 40)
print("      My AI Assistant")
print("=" * 40)

while True:
    user_input = input("\nYou : ")

    # 檢查用戶是否要退出
    if user_input.lower() == "quit":
        print("\nAI  : Goodbye! Have a great day.")
        break

    # 4. 建立用戶問題的嵌入向量
    question_embedding = create_embedding(
        user_input
    )

    # 初始化最佳分數和文件
    best_score = -1
    best_document = None

    # 5. 計算用戶問題和每個文件的相似度
    for filename, embedding in document_embeddings.items():

        # 5.1 計算相似度
        score = cosine_similarity(
            question_embedding,
            embedding
        )

        print(f"{filename}: {score:.4f}")

        # 5.2 更新最佳分數和文件
        if score > best_score:
            best_score = score
            best_document = filename

    # 6. 取得最佳文件的內容
    context = documents[best_document]
    print(f"\nContext: \n{context}")

    # 7. 建立提示 prompt
    prompt = f"""
    請只根據以下資訊
    回答問題。
    
    Context:
    
    {context}
    
    Question:
    
    {user_input}
    """

    # 8. 生成回應
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAI :", response.choices[0].message.content)
