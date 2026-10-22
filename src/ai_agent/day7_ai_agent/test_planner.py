from planner import choose_tool

# 只會回傳工具名稱，不會執行工具
print(
    choose_tool("What time is it?")  # get_current_time
)

print(
    choose_tool("Generate a password")  # generate_password
)

print(
    choose_tool("Roll a dice")  # roll_dice
)

print(
    choose_tool("Explain Python")  # none
)
