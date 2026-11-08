from langgraph.graph import StateGraph, START, END  # 匯入 StateGraph, START, END 類別

from agent.planner import planner
from agent.state import AgentState


# 定義一個名為 create_planner_node 的函數，該函數接受一個工具清單作為參數
# tools = [
#     Tool(name="search", description="搜尋網路資料"),
#     Tool(name="calculator", description="執行數學計算"),
# ]
def create_planner_node(tools):
    # 定義一個名為 planner_node 的函數，該函數接受一個 AgentState 對象作為參數
    # state: AgentState 表示：
    # • state 是這個參數的名稱。
    # • AgentState 是它的型別註記，表示預期傳入的 state 符合 AgentState 所描述的結構。
    # state: AgentState =
    # {
    #     "user_request": "解釋 Python",
    #     "current_step": 0,
    #     "max_steps": 5,
    #     "actions": [],
    #     "observations": [],
    #     "finished": False,
    #     "final_answer": "",
    # }
    def planner_node_fn(state: AgentState):
        action = planner(state, tools)

        print("\nPlanner Selected:")
        print(action)

        return {
            "actions": state["actions"],
            "observations": state["observations"],
            "current_step": state["current_step"],
            "finished": action == "FINISH",
            "final_answer": state["final_answer"]
        }

    # StateGraph(AgentState) 告訴 LangGraph 狀態有哪些欄位；
    # add_node(...) 把 planner_node_fn 註冊為節點。
    # 執行時，LangGraph 會把節點回傳的字典視為 state update：預設情況下，回傳的欄位會覆蓋狀態中同名欄位，沒回傳的欄位則維持原值。
    return planner_node_fn  # 回傳 planner_node_fn 函數，這個函數會被註冊為節點，並在執行時被呼叫。


# 定義一個名為 build_graph 的函數，該函數接受一個工具清單作為參數
def build_graph(tools):
    # 1. 建立一個名為 builder 的 StateGraph 物件，並指定結構描述為 AgentState
    builder = StateGraph(AgentState)

    # 2. 建立 planner_node：create_planner_node(tools) 會回傳一個函數，該函數會被註冊為節點。
    planner_node_fn = create_planner_node(tools)

    # 3. 將 planner_node_fn 註冊為節點，並指定節點名稱為 "planner"
    # 節點函式回傳的更新欄位，必須符合 state schema：回傳的鍵要是 schema 中定義的欄位，值也要符合該欄位的型別。
    builder.add_node("planner", planner_node_fn)
    builder.add_edge(START, "planner")  # 4. 設定圖的入口連到 "planner"，因此圖開始時會執行它
    builder.add_edge("planner", END)  # 5. 設定 "planner" 執行後連到圖的結束點，因此圖會結束

    return builder.compile()  # 6. 編譯圖並回傳
