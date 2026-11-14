from crewai import Task

from agents import researcher, coder, reviewer

research_task = Task(
    description="研究自主 AI agent。說明 agent loop、工具、狀態與觀察結果。在完成任務前，使用 MCP Current Time 工具，並納入工具回傳的時間。",  # 給 agent 的任務指示
    expected_output="一份簡潔的自主 AI agent 技術說明。",  # 期望的輸出結果
    agent=researcher  # 使用的研究員代理
)

coding_task = Task(
    description="根據 researcher 提供的研究內容，撰寫一個簡單的 Python AI agent loop 範例。",
    expected_output="一份完整的 Python 程式碼範例，並附上簡短說明。",
    agent=coder,
    context=[research_task]  # 指定此任務的上下文為 research_task，讓 coder 可以參考研究員的研究結果來撰寫程式碼
)

review_task = Task(
    description="審查 developer 撰寫的 Python 程式碼，找出錯誤並提出改進建議。",
    expected_output="一份程式碼審查，列出發現的問題與改進建議。",
    agent=reviewer,
    context=[coding_task]
)

memory_task = Task(
    description="在我們上一項任務中自我介紹的那個人叫什麼名字？",
    expected_output="那個人的名字。",
    agent=researcher
)
