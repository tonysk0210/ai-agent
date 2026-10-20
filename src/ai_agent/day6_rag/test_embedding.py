from dotenv import load_dotenv
from openai import OpenAI
from similarity import cosine_similarity
import os

load_dotenv()

# 建立一個客戶端，用於與 OpenAI API 進行通訊
client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"]
)

# 建立一個函數，用於生成文本的嵌入向量
def create_embedding(content):
    embedding = client.embeddings.create(
        model="nomic-embed-text-v2-moe",
        input=content
    ).data[0].embedding
    return embedding


# 直接執行此檔案時，才執行下面的嵌入測試；被其他檔案匯入時不執行。
if __name__ == "__main__":
    text1 = "Python is a programming language."
    text2 = "Python is used for software development."

    embedding1 = create_embedding(text1)
    embedding2 = create_embedding(text2)

    print(len(embedding1))
    print(len(embedding2))

    score = cosine_similarity(embedding1, embedding2)
    print("The cosine similarity between the two embeddings is:", score)
