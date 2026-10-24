from task_planner import decompose_task

# 使用者需求
user_request = (
    "取得目前時間、產生一組安全的密碼，並解釋 Python。"
)

tasks = decompose_task(user_request)

print("\nTask Plan")
print("---------")

for task in tasks:
    print("-", task)
