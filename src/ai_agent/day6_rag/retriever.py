from pathlib import Path


# 輸入文件夾路徑，回傳文件名稱和內容的 dictionary
def load_documents():
    documents = {}

    folder = Path("knowledge")

    for file in folder.glob("*.txt"):  # 遍歷資料夾中的所有文字檔
        documents[file.name] = file.read_text(encoding="utf-8")  # 讀取每個檔案的內容

    return documents


# documents = {
#     "python.txt": "Python 是一種程式語言……",
#     "ai.txt": "人工智慧是……"
# }

# 搜尋函數，根據問題回傳相關的文件名稱和內容
def retrieve(question):
    documents = load_documents()
    question = question.lower()

    for filename, content in documents.items():
        # 如果問題出現在文件內容中，則回傳文件名稱和內容
        if question in content.lower():
            return filename, content

    return None, None
