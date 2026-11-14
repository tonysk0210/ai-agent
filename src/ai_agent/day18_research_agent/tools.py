import os
import requests
import json
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

# BeautifulSoup 用來解析 read_webpage() 下載回來的網頁 HTML。
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# 研究筆記清單
research_notes = []
# [
#     {
#         "source": "https://example.com/job",
#         "finding": "職缺要求具備 Python 技能",
#         "evidence": "熟悉 Python 程式設計及相關框架",
#         "verified": False
#     }
# ]
MODEL = "qwen3:1.7b"


# 搜尋網頁
def search_web(query, max_results=5):
    """
    使用 Tavily Search API 搜尋網頁。
    Args:
        query: 搜尋查詢。
        max_results: 搜尋結果的數量上限。
    Returns:
        搜尋結果清單。
    """
    max_results = int(max_results)  # 將 max_results 轉換為整數

    # 從環境變數中取得 Tavily API 金鑰
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "找不到 TAVILY_API_KEY。請在執行環境設定 Tavily API key。"
        )

    # 呼叫 Tavily Search API
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": api_key,
            "query": query,
            "max_results": max_results,
        },
        timeout=30,
    )
    # response = <Response [200]>
    #
    # response.status_code  # HTTP 狀態碼，例如 200
    # response.url          # 最終回應網址
    # response.headers      # 回應標頭
    # response.text         # 解碼後的回應本文；這裡預期是 HTML
    # response.content      # 回應本文的 bytes 版本

    response.raise_for_status()
    payload = response.json()  # 解析 JSON 格式的回應本文
    # payload = {
    #     "query": "AI agents software development",
    #     "results": [
    #         {
    #             "title": "搜尋結果標題",
    #             "url": "https://example.com/article",
    #             "content": "搜尋結果的文字摘要",
    #             "score": 0.92
    #         }
    #     ],
    #     "response_time": 0.8,
    #     "request_id": "示意用的請求 ID"
    # }

    return [
        {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
        }
        for result in payload.get("results", [])[:max_results]
    ]
    # [
    #     {
    #         "title": "搜尋結果標題",
    #         "url": "https://example.com/article",
    #         "snippet": "搜尋結果摘要"
    #     },
    #     {
    #         "title": "另一筆搜尋結果標題",
    #         "url": "https://example.org/page",
    #         "snippet": "另一筆搜尋結果摘要"
    #     }
    # ]

    # 這相當於以下較展開的寫法：
    # output = []
    #
    # for result in payload.get("results", [])[:max_results]:
    #     item = {
    #         "title": result.get("title", ""),
    #         "url": result.get("url", ""),
    #         "snippet": result.get("content", ""),
    #     }
    #     output.append(item)
    #
    # return output


# 讀取網頁
def read_webpage(url):
    """
    下載網頁並擷取其文字內容。
    Args:
        url: 網頁網址。
    Returns:
        擷取出的網頁文字內容。
    """

    if url.startswith("//"):
        url = "https:" + url

    parsed_url = urlparse(url)
    if "duckduckgo.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)
        if "uddg" in params:
            url = params["uddg"][0]  # 'https://example.com/article?id=42'

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20
    )
    # response 物件 = <Response 200>
    #
    # response.status_code  # 200，HTTP 狀態碼
    # response.url          # 最後回應的網址
    # response.headers      # 回應標頭
    # response.text         # 解碼後的回應內容，這裡通常是 HTML
    # response.content      # 回應內容的 bytes 版本

    response.raise_for_status()  # 如果回應狀態碼不是 200，則 raise 一個異常

    soup = BeautifulSoup(response.text, "html.parser")
    # <html>
    #   <body>
    #     <h1>新聞</h1>
    #     <p>第一段內容。</p>
    #     <script>追蹤程式碼</script>
    #     <style>body { color: black; }</style>
    #     <p>第二段內容。</p>
    #   </body>
    # </html>

    # [
    #     <script>...</script>,
    #     <style>...</style>
    # ]
    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    text = soup.get_text("\n", strip=True)
    # text =
    # 新聞
    # 第一段內容。
    # 第二段內容。

    return text[:12000]  # 回傳前 12000 個字元


# 記錄研究發現
def add_research_note(source, finding, evidence):
    """
    記錄一項重要的研究發現。

    Args:
        source: 來源的網址或名稱。
        finding: 從來源中擷取出的具體主張或結論。
        evidence: 來源中支持此研究發現的文字或資訊。

    Returns:
        確認訊息。
    """

    # 將研究發現加入清單
    research_notes.append({
        "source": source,
        "finding": finding,
        "evidence": evidence,
        "verified": False
    })

    # 回傳確認訊息
    return {
        "status": "stored",
        "finding": finding
    }


# 取得研究筆記
def get_research_notes():
    """
    回傳目前為止收集到的所有研究筆記。
    """

    return [note.copy() for note in research_notes]  # 回傳研究筆記的副本


# [
#     {
#         "source": "https://example.com/job",
#         "finding": "職缺要求具備 Python 技能",
#         "evidence": "熟悉 Python 程式設計及相關框架",
#         "verified": False
#     }
# ]

# 標記研究筆記為已驗證
def mark_note_verified(source, finding):
    """
    將符合條件的研究筆記標記為已驗證。
    """
    for note in research_notes:

        if (note["source"] == source and note["finding"] == finding):
            note["verified"] = True

            return {
                "status": "verified",
                "finding": finding
            }

    return {
        "status": "not_found",
        "finding": finding
    }


# 取得已驗證的研究筆記
def get_verified_research_notes():
    """
    僅回傳已驗證的研究筆記。
    """

    return [
        note.copy()  # 把符合條件的筆記複製一份
        for note in research_notes  # 逐筆查看研究筆記
        if note.get("verified", False)  # 只保留 verified 為 True 的筆記；這裡的 False 是預設值
    ]
# [
#     {"finding": "要求 Python 技能", "verified": True}
# ]
