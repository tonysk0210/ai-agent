from crewai import Crew, Process

from agents import researcher, coder, reviewer
from tasks import research_task, coding_task, review_task
from llm import manager_llm

# 創建一個 Crew，包含三個代理人（研究員、開發者、審查者）和三個任務（研究、編碼、審查），並設定執行流程為順序執行。
crew = Crew(
    agents=[researcher, coder, reviewer],
    tasks=[research_task, coding_task, review_task],
    # process=Process.sequential,  # 設定流程為順序執行，依 tasks 清單的順序逐項執行。你的清單是研究、編碼、審查，因此會按這個順序進行
    process=Process.hierarchical,  # 設定流程為階層式執行，由 manager_llm 管理員決定如何分派與協調
    manager_llm=manager_llm,  # 設定管理員 LLM
    verbose=True  # 開啟較詳細的執行輸出，方便觀察進度
)
