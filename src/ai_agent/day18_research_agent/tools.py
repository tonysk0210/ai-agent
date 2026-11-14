import requests
# BeautifulSoup(response.text, "html.parser") 會解析下載回來的網頁 HTML；
# 之後的 soup.select(...) 和 select_one(...) 再從中找出搜尋結果的標題、連結和摘要。
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


# 搜尋網頁
def search_web(query, max_results=5):
    """
    使用 DuckDuckGo 搜尋網頁。
    Args:
        query: 搜尋查詢。
        max_results: 搜尋結果的數量上限。
    Returns:
        搜尋結果清單。
    """

    response = requests.get(
        "https://html.duckduckgo.com/html/",
        params={"q": query},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # [
    #     <div class="result">第一筆結果的 HTML...</div>,
    #     <div class="result">第二筆結果的 HTML...</div>,
    # ]
    for result in soup.select(".result")[:max_results]:

        # title_element = <某個 HTML 標籤 class="result__title">標題內容</某個 HTML 標籤>
        # link_element = <某個 HTML 標籤 class="result__a" href="https://example.com">連結文字</某個 HTML 標籤>
        # snippet_element = <某個 HTML 標籤 class="result__snippet">摘要內容</某個 HTML 標籤>
        title_element = result.select_one(".result__title")
        link_element = result.select_one(".result__a")
        snippet_element = result.select_one(".result__snippet")

        # 如果沒有連結，則跳過此結果
        if not link_element:
            continue

        results.append({
            "title": (title_element.get_text(" ", strip=True)
                      if title_element
                      else ""
                      ),
            "url": link_element.get("href", ""),
            "snippet": (snippet_element.get_text(" ", strip=True)
                        if snippet_element
                        else ""
                        )
        })
        # results = [
        #     {
        #         "title": "第一筆搜尋結果的標題",
        #         "url": "https://example.com/page1",
        #         "snippet": "第一筆搜尋結果的摘要"
        #     },
        #     {
        #         "title": "第二筆搜尋結果的標題",
        #         "url": "https://example.com/page2",
        #         "snippet": "第二筆搜尋結果的摘要"
        #     }
        # ]

    return results


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
