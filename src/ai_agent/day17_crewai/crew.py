from crewai import Crew, Process

from agents import researcher, coder, reviewer
from tasks import research_task, coding_task, review_task, memory_task
from llm import manager_llm

# 創建一個 Crew，包含三個代理人（研究員、開發者、審查者）和三個任務（研究、編碼、審查），並設定執行流程為順序執行。
crew = Crew(
    agents=[researcher, coder, reviewer],
    tasks=[research_task, coding_task, review_task],
    # process=Process.sequential,  # 設定流程為順序執行，依 tasks 清單的順序逐項執行。你的清單是研究、編碼、審查，因此會按這個順序進行
    process=Process.hierarchical,  # 設定流程為階層式執行，由 manager_llm 管理員決定如何分派與協調
    manager_llm=manager_llm,  # 設定管理員 LLM
    memory=True, embedder={
        "provider": "ollama",
        "config": {
            "model_name": "nomic-embed-text-v2-moe",
            "url": "http://localhost:11434/api/embeddings"
        }
    },  # CrewAI 會建立一個由 crew 共用的記憶庫；預設使用向量 embedding 搜尋，依查詢找出相關內容
    verbose=True  # 開啟較詳細的執行輸出，方便觀察進度
)

# • http://localhost:11434/v1 是 Ollama 提供的 OpenAI 相容 API 基底網址。OpenAI client 會依照 embeddings.create(...) 等呼叫補上對應路徑。api_key="ollama" 是 client 初始化時需要的佔位值，Ollama 本機 API 通常不會用它驗證。
# • http://localhost:11434/api/embed 是 Ollama 原生的 embedding endpoint。crew.py 把它提供給 CrewAI 的 Ollama embedder。

# 創建一個新的 Crew，專門處理記憶任務
memory_crew = Crew(
    agents=[researcher],
    tasks=[memory_task],
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model_name": "nomic-embed-text-v2-moe",
            "url": "http://localhost:11434/api/embeddings"
        }
    },
    verbose=True
)

# memory=True 使用 CrewAI 的統一記憶系統，預設儲存後端是 LanceDB；記憶資料存放在 CrewAI 的資料目錄下，或在設定 CREWAI_STORAGE_DIR 時存到該目錄的 memory 子目錄。
# CrewAI 儲存設定 執行時仍會使用 RAM，例如載入記憶系統、產生 embedding、查詢記憶。但 Ollama 服務收到文字後產生的 embedding，會連同記憶資料由儲存後端保存；程式結束後，磁碟上的記憶仍可留存。
