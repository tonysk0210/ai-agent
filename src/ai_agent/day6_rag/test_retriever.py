from retriever import load_documents, retrieve  # 輸入 retriever.py 模組中的 load_documents 函數

documents = load_documents()  # 呼叫 load_documents 函數，將回傳的文件內容存儲在 documents dictionary 變數中

for name, text in documents.items():  # documents.items() 每次會取出一組 key 和 value，並分別放進 name 和 text：
    print(name)  # 印出文件名
    print(text)  # 印出文件內容
    print("-" * 40)

# 搜尋函數，根據問題回傳相關的文件名稱和內容
filename, content = retrieve("Python")
print(filename)
print()
print(content)
