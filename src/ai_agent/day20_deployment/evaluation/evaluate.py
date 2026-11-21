def check_tool(result, expected_tool):
    for message in result["messages"]:

        # 這段代码检查消息中是否包含工具调用
        tool_calls = getattr(message, "tool_calls", [])

        for call in tool_calls:
            if call["name"] == expected_tool:
                return True
    return False

# result = {
#     "messages": [
#         HumanMessage(
#             content="Roll a dice."
#         ),
#         AIMessage(
#             content="",
#             tool_calls=[
#                 {
#                     "name": "roll_dice",
#                     "args": {},
#                     "id": "call_123",
#                     "type": "tool_call",
#                 }
#             ],
#         ),
#         ToolMessage(
#             content="4",
#             name="roll_dice",
#             tool_call_id="call_123",
#         ),
#         AIMessage(
#             content="You rolled a 4."
#         ),
#     ]
# }