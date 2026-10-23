from ai_agent.day9_agent_loop.mcp_client import execute_tool


# 定義執行動作的函數，接收動作 action (tool_name) 和 Client 物件為參數，回傳動作的執行結果
async def execute_action(action, client):
    # 1. 執行動作
    result = await execute_tool(client, action)

    # result = CallToolResult(
    #     content=[
    #         TextContent(type="text", text="產生的密碼是 abc123")
    #     ],
    #     isError=False
    # )

    # 2. 檢查結果是否有內容
    if hasattr(result, "content"):

        # 3. 如果有內容，回傳內容
        if result.content:
            return result.content[0].text

    # 4. 如果沒有內容，回傳結果
    return str(result)
