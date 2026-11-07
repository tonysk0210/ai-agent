TOOL_PERMISSIONS = {
    "research": {"get_weather", "read_file"},
    "coding": {"read_file"},
    "review": {"read_file"},
    "manager": {"get_weather", "read_file"}
}


# 這是一個用於檢查代理是否被允許使用特定工具的函數
def is_tool_allowed(agent_name, tool_name):
    allowed_tools = (TOOL_PERMISSIONS.get(agent_name, set()))  # 取得代理被允許使用的工具，否則回傳空集合
    return tool_name in allowed_tools  # 檢查工具是否在被允許的工具集合中 true / false


# 這是一個用於展示權限的函數
def demonstrate_permissions():
    # 這是一個包含代理和工具組合的清單
    examples = [
        ("research", "read_file"),
        ("coding", "get_weather"),
        ("review", "read_file"),
        ("manager", "get_weather")
    ]

    print("\n權限示範")
    print("-" * 30)

    # 這是一個迴圈，用於檢查每個代理和工具的組合
    # agent_name = "review"
    # tool_name = "read_file"
    # 下一個 tuple 會進入下一輪，重新指定這兩個變數。這種寫法叫做序列解包（unpacking）：每個元素必須剛好提供兩個值，才能分別放入 agent_name 和 tool_name。
    for agent_name, tool_name in examples:
        allowed = is_tool_allowed(agent_name, tool_name)  # 檢查代理是否被允許使用該工具

        print(
            f"{agent_name:10} -> "
            f"{tool_name:12} : "
            f"{'ALLOWED' if allowed else 'DENIED'}"
        )
