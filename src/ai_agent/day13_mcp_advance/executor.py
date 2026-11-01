from mcp_manager import run_tool


# action (returned value from planner) =
# {
#     "tool": "tool_name",
#     "arguments": {
#         "argument_name": "argument_value"
#     }
# }
# or
# {
#     "tool": "FINISH",
#     "arguments": {}
# }

async def execute_action(action, tool_registry):
    tool_name = action["tool"]  # 取得工具名稱
    arguments = action.get("arguments", {})  # 取得工具參數

    result = await run_tool(tool_registry, tool_name, arguments)
    # result =
    # CallToolResult(
    #     content=[
    #         TextContent(
    #             type='text',
    #             text='Sunny, 32°C',
    #             annotations=None,
    #             meta=None
    #         )
    #     ],
    #     structured_content=None,
    #     data=None,
    #     is_error=False,
    #     meta={
    #         'io.modelcontextprotocol/serverInfo': {
    #             'name': 'Weather Server',
    #             'version': '4.1.3'
    #         }
    #     }
    # )

    if hasattr(result, "content"):

        if result.content:
            return result.content[0].text

    return str(result)  # 'Sunny, 32°C'
