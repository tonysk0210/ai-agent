from langgraph.graph import StateGraph, START, END  # 匯入 StateGraph, START, END 類別

from agent.planner import planner
from agent.executor import execute_action
from agent.state import AgentState
from agent.runner import format_answer


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
    #     "action": "",
    #     "finished": False,
    #     "final_answer": "",
    # }
    def planner_node_fn(state: AgentState):
        action = planner(state, tools)

        print("\nPlanner Selected:")
        print(action)

        return {
            "action": action,
            "finished": action == "FINISH"
        }

    # StateGraph(AgentState) 告訴 LangGraph 狀態有哪些欄位；
    # add_node(...) 把 planner_node_fn 註冊為節點。
    # 執行時，LangGraph 會把節點回傳的字典視為 state update：預設情況下，回傳的欄位會覆蓋狀態中同名欄位，沒回傳的欄位則維持原值。
    return planner_node_fn  # 回傳 planner_node_fn 函數，這個函數會被註冊為節點，並在執行時被呼叫。


# 定義一個名為 create_tool_node 的函數，該函數接受一個 Client 物件作為參數，回傳一個工具節點函數
def create_tool_node(client):
    async def tool_node_fn(state: AgentState):
        # 1. 從 state 取得 action
        action = state["action"]

        # 2. 執行 action 並取得 observation
        observation = await execute_action(action, client)

        print("\nTool Observation:")
        print(observation)

        # 3. 回傳更新的 state，包含 observation、actions 和 current_step
        return {
            "observations": (
                    state["observations"]
                    + [
                        {
                            "step": state["current_step"],
                            "action": action,
                            "observation": observation
                        }
                    ]
            ),
            "actions": (state["actions"] + [action]),
            "current_step": (state["current_step"] + 1)
        }

    return tool_node_fn  # 回傳 tool_node_fn 函數，這個函數會被註冊為節點，並在執行時被呼叫。


# tool_node_fn =
# {
#     "observations": [
#         {
#             "step": 0,
#             "action": "current_time",
#             "observation": "2026-11-09 10:30"
#         }
#     ],
#     "actions": ["current_time"],
#     "current_step": 1
# }

# observations =
# [
#     {"step": 0, "action": "search", "observation": "找到資料"},
#     {"step": 1, "action": "current_time", "observation": "10:30"}
# ]
#
# items = ["a", "b"]
# items = items + ["c"]
#
# items 是 ["a", "b", "c"]

# 定義一個名為 answer_node 的函數，該函數接受一個 AgentState 對象作為參數，回傳最終答案和 finished 狀態
def answer_node(state: AgentState):
    # 1. 呼叫 format_answer 函數格式化答案
    answer = format_answer(state)

    print("\nFinal Answer:")
    print(answer)

    return {
        "final_answer": answer,
        "finished": True
    }


# 定義一個名為 route_after_planner 的函數，該函數接受一個 AgentState 對象作為參數，回傳 "finish" 或 "tool" 字串
def route_after_planner(state: AgentState):
    if state["action"] == "FINISH":
        return "finish"
    return "tool"


# 定義一個名為 route_after_tool 的函數，該函數接受一個 AgentState 對象作為參數，回傳 "stop" 或 "continue" 字串
def route_after_tool(state: AgentState):
    if (state["current_step"] >= state["max_steps"]):
        return "stop"
    return "continue"


# 定義一個名為 build_graph 的函數，該函數接受一個工具清單作為參數
def build_graph(tools, client):
    # 1. 建立一個名為 builder 的 StateGraph 物件，並指定結構描述為 AgentState
    builder = StateGraph(AgentState)

    # 2. 建立 planner_node：create_planner_node(tools) 會回傳一個函數，該函數會被註冊為節點。
    # 節點函式回傳的更新欄位，必須符合 state schema：回傳的鍵要是 schema 中定義的欄位，值也要符合該欄位的型別。
    builder.add_node("planner", create_planner_node(tools))
    # 3. 建立 tool_node：create_tool_node(client) 會回傳一個函數，該函數會被註冊為節點。
    builder.add_node("tool", create_tool_node(client))
    # 4. 建立 answer_node：answer_node 會回傳最終答案和 finished 狀態
    builder.add_node("answer", answer_node)

    # 5. 增加條件邊，根據 route_after_planner 的回傳值決定下一步要執行的節點
    builder.add_conditional_edges(
        "planner",  # 從 planner 節點開始判斷
        route_after_planner,  # 接收 state，回傳路由標籤
        {
            "tool": "tool",  # 回傳 "tool" → 前往名為 tool 的節點
            "finish": "answer"  # 回傳 "finish" → 前往名為 answer 的節點
        }
    )

    # 6. 增加條件邊，根據 route_after_tool 的回傳值決定下一步要執行的節點
    builder.add_conditional_edges(
        "tool",  # 從 tool 節點開始判斷
        route_after_tool,  # 接收 state，回傳路由標籤
        {
            "continue": "planner",  # 回傳 "continue" → 前往名為 planner 的節點
            "stop": "answer"  # 回傳 "stop" → 前往名為 answer 的節點
        }
    )
    builder.add_edge(START, "planner")  # 7. 設定圖的入口連到 "planner"，因此圖開始時會執行它
    builder.add_edge("answer", END)  # 8. 設定 "answer" 執行後連到圖的結束點，因此圖會結束

    return builder.compile()  # 9. 編譯圖並回傳
