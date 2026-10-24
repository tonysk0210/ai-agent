# 建立狀態 update
def create_state(user_request, max_steps=5):
    return {
        "user_request": user_request,
        "tasks": [],
        "current_task": None,
        "current_step": 0,
        "max_steps": max_steps,
        "actions": [],
        "observations": [],
        "results": [],
        "finished": False,
        "final_answer": ""
    }


# 增加任務 update
def add_task(state, task):
    state["tasks"].append({
        "task": task,
        "status": "pending"
    })


# 完成任務 update
def complete_task(state, task):
    # 這邊將任務進行正規化，無論輸入的格式如何，都能正確比較 ("Generate password", "generate password", "generate_password")
    normalized_task = task.strip().lower().replace("_", " ")

    for item in state["tasks"]:

        normalized_existing_task = item["task"].strip().lower().replace("_", " ")

        # 比較正規化後的任務是否一致，如果一致則將該任務狀態設為完成
        if normalized_existing_task == normalized_task:
            item["status"] = "completed"
            return True
    return False


# 增加結果 update
def add_result(state, result):
    state["results"].append(result)


# 取得未完成的任務 update
def get_pending_tasks(state):
    return [
        item["task"]  # 放進結果串列的值
        for item in state["tasks"]  # 逐筆取出任務
        if item["status"] == "pending"  # 只保留待處理的任務
    ]


# state["tasks"] = [
#     {"task": "產生密碼", "status": "pending"},
#     {"task": "解釋 Python", "status": "completed"}
# ]
#
# get_pending_tasks 會逐筆檢查 item，只保留狀態是 "pending" 的任務，再取出其中的 "task" 值。結果是：["產生密碼"]


# 判斷是否所有任務都已完成 update
def all_tasks_completed(state):
    if not state["tasks"]:
        return False

    return all(
        item["status"] == "completed"
        for item in state["tasks"]
    )


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
