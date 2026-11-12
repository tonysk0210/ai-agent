from crewai import Agent
from llm import llm

# verbose=True 讓 CrewAI 在 Agent 執行任務時，輸出較詳細的過程紀錄到終端機，例如目前的執行步驟、工具使用情況和結果。
# role、goal、backstory 都是 Agent 設定，但 prompt 還會包含任務與工具等資訊。可以把 role、goal 和 backstory 看成 system prompt 的重要素材，三者共同塑造 Agent 的 system prompt，而不是它們本身就等於完整的 system prompt。
# • role：AI 研究員、Python 開發者或程式碼審查者等角色定位。
# • goal：這個角色要達成的目標。
# • backstory：補充角色背景與專長，影響它處理任務的方式。

# 創建一個研究員代理
researcher = Agent(
    role="AI 研究員",
    goal="研究 AI agent 的概念，並提供準確的資訊。",
    backstory="你是一位 AI 研究員，專精於 AI agent。",
    llm=llm,
    verbose=True  # 詳細模式
)

# 創建一個開發者代理
coder = Agent(
    role="Python 開發者",
    goal="根據研究結果撰寫清楚且正確的 Python 程式碼。",
    backstory="你是一位經驗豐富的 Python 開發者，擅長撰寫簡潔且實用的程式碼。",
    llm=llm,
    verbose=True  # 詳細模式
)

# 創建一個審查者代理
reviewer = Agent(
    role="程式碼審查者",
    goal="審查產生的程式碼，並找出其中的問題。",
    backstory="你是一位資深的 Python 審查者，重視程式碼的正確性與品質。",
    llm=llm,
    verbose=True  # 詳細模式
)
