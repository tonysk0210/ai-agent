from typing import TypedDict


# AgentState(TypedDict) 不是要把 state 建立成一般的 class 物件，而是用來描述字典應該有哪些欄位，以及各欄位的型別。
# 用 class 的語法，宣告一種名為 AgentState 的字典結構。
class AgentState(TypedDict):
    user_request: str
    current_step: int
    max_steps: int
    actions: list
    observations: list
    action: str
    finished: bool
    final_answer: str


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


# 建立狀態
def create_state(user_request, max_steps=5):
    return {
        "user_request": user_request,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "finished": False,
        "final_answer": ""
    }


# 記錄動作
def add_action(state, action):
    state["actions"].append(action)


# 記錄觀察值
def record_observation(state, action, observation):
    state["observations"].append(
        {
            "step": state["current_step"],  # 當前步數
            "action": action,  # 動作
            "observation": observation  # 觀察值
        }
    )


# 遷移到下一個步驟
def next_step(state):
    state["current_step"] += 1


# 是否可以繼續
def can_continue(state):
    return (
            not state["finished"]  # 是否完成
            and state["current_step"] < state["max_steps"]  # 是否在最大步數內
    )


# 終了狀態
def finish(state, answer):
    state["final_answer"] = answer
    state["finished"] = True
