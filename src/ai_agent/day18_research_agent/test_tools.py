from tools import search_web, read_webpage

results = search_web("AI agents software development", max_results=3)

print("\n===== SEARCH RESULTS =====\n")

if not results:
    print("沒有找到搜尋結果。")

for result in results:
    print("===== TITLE =====")
    print(result["title"])
    print("===== URL =====")
    print(result["url"])
    print("===== SNIPPET =====")
    print(result["snippet"])
    print()

if results:
    text = read_webpage(results[0]["url"])  # 只讀取第一個搜尋結果的網頁內容
    print("\n===== WEBPAGE TEXT=====\n")
    print(text[:2000])
