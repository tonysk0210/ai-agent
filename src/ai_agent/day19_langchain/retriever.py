from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 1. 建立文字文件載入器
loader = TextLoader("notes.txt", encoding="utf-8")
# 2. 載入內容並回傳 Document 清單
documents = loader.load()
# 3. 建立文本分割器
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
# 4. 分割文本
chunks = splitter.split_documents(documents)
# chunks = [
#     Document(
#         page_content="第一段切分後的文字……",
#         metadata={"source": "notes.txt"}
#     ),
#     Document(
#         page_content="第二段切分後的文字……",
#         metadata={"source": "notes.txt"}
#     ),
# ]

# 5. 建立 Ollama 嵌入模型介面
embeddings = OllamaEmbeddings(model="nomic-embed-text-v2-moe")

# 6. 建立向量存儲 - 將文件轉成向量並加入 FAISS 索引 - 建立的 FAISS 向量存儲預設放在目前 Python 程序的 RAM 裡
vector_store = FAISS.from_documents(chunks, embeddings)

# 7. 建立检索器 - 建立向量存儲的檢索器
retriever = vector_store.as_retriever()
