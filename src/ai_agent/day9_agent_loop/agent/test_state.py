from ai_agent.day9_agent_loop.agent.state import *

# 創建狀態
state = create_state("產生一組密碼並告訴我目前時間。")

print("初始狀態")
print(state)

# 增加動作
add_action(
    state,
    "generate_password"
)

# 增加觀察值
record_observation(
    state,
    "generate_password",
    "密碼：X#8Lm@4P"
)

# 遷移到下一個步驟
next_step(state)

print("\n執行一次迭代後的狀態")
print(state)

# 終了狀態
finish(
    state,
    "密碼：X#8Lm@4P\n目前時間：上午 10:35"
)

print("\n最終狀態")
print(state)
