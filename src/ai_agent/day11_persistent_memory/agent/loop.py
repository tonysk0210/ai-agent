from state import (
    create_state,
    add_task,
    add_action,
    record_observation,
    add_result,
    complete_task,
    all_tasks_completed,
    next_step,
    can_continue,
    finish
)  # 載入狀態相關函數
from task_planner import decompose_task  # 載入任務分解函數


# 解析決策 decision = "TASK: 取得目前時間\nTOOL: get_current_time"
def parse_decision(decision):
    task = None
    tool = None

    for line in decision.splitlines():  # 把字串拆成多行
        line = line.strip()  # 去掉每行前後的空白
        if line.startswith("TASK:"):  # 如果一行以 "TASK:" 開頭，就用 line[5:] 去掉前綴，取出 "取得目前時間"，存進 task
            task = line[5:].strip()
        elif line.startswith("TOOL:"):  # 如果一行以 "TOOL:" 開頭，同樣取出 "get_current_time"，存進 tool
            tool = line[5:].strip()

    # 例如模型意外回傳：TASK: "取得目前時間 TOOL: get_current_time"
    if task and "TOOL:" in task:
        parts = task.split("TOOL:", 1)  # parts = ["取得目前時間 ", " get_current_time"]
        task = parts[0].strip()  # task = "取得目前時間"
        if not tool:
            tool = parts[1].strip()  # tool = "get_current_time"

    return task, tool


# 運行代理循環
async def run_agent_loop(
        user_request,
        planner,  # 調用 planner function 決定下一步要執行什麼
        execute_action,  # 調用 execute_action function 執行動作
        format_answer,  # 調用 format_answer function 格式化答案
        tools,
        client
):
    # 1. 創建狀態
    state = create_state(user_request)

    # 2. 生成計劃任務
    planned_tasks = decompose_task(user_request)

    # 3. 增加計劃任務
    for task in planned_tasks:
        add_task(state, task)

    print("\nTask Plan")
    print("---------")
    # 印出計劃任務
    for item in state["tasks"]:
        print("-", item["task"])

    # 4. 當 can_continue 時: "這是我們代理的心臟“
    while can_continue(state):

        print("*" * 40, "\n")
        print("* 當前 State:", state)  # 印出當前狀態

        # --------------------------------
        # Check whether all tasks are done
        # --------------------------------
        # 5. 如果所有任務都完成了，我們格式化答案並結束
        if all_tasks_completed(state):
            print(
                "\n--- Step "
                f"{state['current_step'] + 1} ---"
            )
            print("Planner Decision:")
            print("TASK: FINISH")
            answer = format_answer(state)
            finish(state, answer)  # 6. 終了狀態
            print("* 當前 State @ FINISH:", state)  # 印出當前狀態
            break

        print(
            f"\n--- Step "
            f"{state['current_step'] + 1} ---"
        )

        # --------------------------------
        # Ask planner for next task
        # --------------------------------
        # 調用 planner 決定下一步要執行什麼
        decision = planner(state, tools)
        print("** Planner Selected:", decision)

        # --------------------------------
        # Check FINISH
        # --------------------------------
        if decision.strip().upper() == "FINISH":
            answer = format_answer(state)
            finish(state, answer)  # 7. 終了狀態
            print("* 當前 State @ FINISH:", state)
            break

        # --------------------------------
        # Extract task and tool
        # --------------------------------
        # 8. 解析決策
        task, tool = parse_decision(decision)
        if not task or not tool:  # 如果沒有任務或工具，增加結果
            add_result(state, "Invalid planner decision.")  # 9. 增加結果
            next_step(state)  # 10. 遷移到下一個步驟
            continue
        state["current_task"] = task

        # --------------------------------
        # Execute tool
        # --------------------------------
        # 執行工具
        observation = await execute_action(tool, client)
        print("Observation:", observation)

        # --------------------------------
        # Update state
        # --------------------------------
        # 11. 增加動作
        add_action(state, tool)

        # 12. 記錄觀察值
        record_observation(state, tool, observation)

        # 13. 增加結果
        add_result(state, observation)

        # --------------------------------
        # Mark task complete
        # --------------------------------
        if not observation.lower().startswith("error"):
            complete_task(state, task)  # 14. 標記任務完成
            print("task completed")  # 印出完成
        else:
            add_result(state, "The previous action failed. The planner must reconsider.")

        # 6. 遷移到下一個步驟
        next_step(state)

    # 回傳狀態
    return state
