# 用於驗證任務的函數
def validate_task(task):
    if not task:
        raise ValueError("Task cannot be empty.")

    task = task.strip()

    if len(task) > 5000:
        raise ValueError("Task is too long.")

    return task
