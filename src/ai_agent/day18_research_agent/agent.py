from ollama import chat
from tools import search_web, read_webpage

MODEL = "qwen3:4b"

# 可用的工具函數
AVAILABLE_TOOLS = {
    "search_web": search_web,
    "read_webpage": read_webpage
}

# 可用的工具函數清單
TOOLS = [search_web, read_webpage]


# 研究代理
def research_agent(user_request):
    # 設定初始消息
    messages = [
        {
            "role": "user",
            "content": user_request
        }
    ]

    while True:

        response = chat(model=MODEL, messages=messages, tools=TOOLS)
        # response = ChatResponse(
        #     message=Message(
        #         role="assistant",
        #         content="AI agent 是能觀察環境並採取行動的系統。",
        #         tool_calls=None
        #     )
        # )

        messages.append(response.message)
        # messages = [
        #     {"role": "user", "content": "請研究 AI agents"},   # dict
        #     Message(                                          # Message 物件
        #         role="assistant",
        #         content="",
        #         tool_calls=[
        #             ToolCall(
        #                 function=Function(
        #                     name="search_web",
        #                     arguments={"query": "AI agents", "max_results": 3} # arguments 來自模型根據問題決定是否呼叫工具，並填入參數
        #                 )
        #             )
        #         ]
        #     )
        # ]

        if not response.message.tool_calls:
            print("\n未呼叫工具，正在回傳最終答案。")
            return response.message.content  # 回傳最終答案

        # 如果有工具呼叫
        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name  # 取得工具名稱
            arguments = tool_call.function.arguments  # 取得工具參數

            print(f"\nCalling tool: {tool_name}")
            print(f"Arguments: {arguments}")

            tool_function = AVAILABLE_TOOLS.get(tool_name)  # 取得工具函數 search_web, read_webpage

            # 如果工具函數不存在
            if tool_function is None:
                result = f"Unknown tool: {tool_name}"
            else:
                result = tool_function(**arguments)  # 呼叫工具函數
                # 其中 **arguments 會把字典展開成關鍵字參數，等同於：
                # result = search_web(query="AI agents", max_results=3)

            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_name": tool_name
            })
            # messages = [
            #     {"role": "user", "content": "請搜尋 AI agents"},
            #
            #     # 前面也會 append 模型回傳的 response.message
            #     Message(
            #         role="assistant",
            #         content="",
            #         tool_calls=[...]
            #     ),
            #
            #     # 這次 append 新增的工具結果
            #     {
            #         "role": "tool",
            #         "content": "搜尋結果……",
            #         "tool_name": "search_web"
            #     }
            # ]
