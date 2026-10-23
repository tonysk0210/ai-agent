from state import (
    create_state,
    add_action,
    record_observation,
    next_step,
    can_continue,
    finish
)  # 載入狀態相關函數


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

    # 2. 當 can_continue 時: "這是我們代理的心臟“
    while can_continue(state):

        print("* 當前 State:", state)  # 印出當前狀態

        # 調用 planner 決定下一步要執行什麼
        action = planner(state, tools)
        print("** Planner Selected:", action)

        # 如果動作是 "FINISH"，我們格式化答案並結束
        if action == "FINISH":
            answer = format_answer(state)
            finish(state, answer)  # 3. 終了狀態

            print("* 當前 State @ FINISH:", state)  # 印出當前狀態
            break

        # 執行動作
        observation = await execute_action(action, client)

        # 4. 增加動作
        add_action(state, action)

        # 5. 記錄觀察值
        record_observation(state, action, observation)

        # 6. 遷移到下一個步驟
        next_step(state)

    # 回傳狀態
    return state
