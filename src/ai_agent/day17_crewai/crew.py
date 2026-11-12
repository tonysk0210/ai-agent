from crewai import Crew, Process

from agents import researcher, coder, reviewer
from tasks import research_task, coding_task, review_task

# 創建一個 Crew，包含三個代理人（研究員、開發者、審查者）和三個任務（研究、編碼、審查），並設定執行流程為順序執行。
crew = Crew(
    agents=[researcher, coder, reviewer],
    tasks=[research_task, coding_task, review_task],
    process=Process.sequential,  # 設定流程為順序執行，前一項任務完成後，才進入下一項
    verbose=True  # 開啟較詳細的執行輸出，方便觀察進度
)
