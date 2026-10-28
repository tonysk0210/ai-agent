from pathlib import Path

from advanced_rag import build_rag, retrieve
from generator import generate_answer

# 文件路徑
DOCUMENT_PATH = Path("documents") / "python.txt"


def main():
    # 1. 讀取文件內容
    text = DOCUMENT_PATH.read_text(encoding="utf-8")
    print("Building RAG knowledge base...")

    # 2. 建立 RAG 知識庫
    build_rag(text, DOCUMENT_PATH.name)
    print("\nAdvanced RAG is ready.")

    while True:
        # 3. 輸入問題
        query = input("\nYou : ").strip()

        # 4. {"exit", "quit"} 是 Python 的 set（集合）
        if query.lower() in {"exit", "quit"}:
            break

        # 6. 搜尋相關文件
        #     # 根據 llm 重新排序（0 到 100 的相關性分數），返回前 3 個　請給出
        #     # [
        #     #     {
        #     #         "text": "第一段 chunk 的文字",
        #     #         "source": "example.txt",
        #     #         "chunk_id": 0,
        #     #         "semantic_score": 0.80,
        #     #         "keyword_score": 0.50,
        #     #         "combined_score": 0.71,
        #     #         "rerank_score": 92.0
        #     #     },
        #     #     {
        #     #         "text": "第二段 chunk 的文字",
        #     #         "source": "example.txt",
        #     #         "chunk_id": 1,
        #     #         "semantic_score": 0.75,
        #     #         "keyword_score": 0.30,
        #     #         "combined_score": 0.62,
        #     #         "rerank_score": 75.0
        #     #     }
        #     # ]
        results = retrieve(query, top_k=5)
        # Retrieved Sources Candidates: retrieve(query, top_k=5):
        # Retrieved Sources Ranking: rerank(query, hybrid_searched_chunks, top_k=3):
        print("\nRetrieved Sources Ranking:")

        # 7. 印出相關文件
        for result in results:
            print(
                f"- "
                f"{result['source']} "
                f"(chunk "
                f"{result['chunk_id']})"
            )

        # 8. 生成答案
        answer = generate_answer(query, results)

        print("\nRAG :")
        print(answer)


if __name__ == "__main__":
    main()
