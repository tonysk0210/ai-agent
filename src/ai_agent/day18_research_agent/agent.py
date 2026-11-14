from ollama import chat
from tools import search_web, read_webpage, add_research_note, get_research_notes

MODEL = "qwen3:1.7b"

# 可用的工具函數
AVAILABLE_TOOLS = {
    "search_web": search_web,
    "read_webpage": read_webpage,
    "add_research_note": add_research_note,
    "get_research_notes": get_research_notes,
}

# 可用的工具函數清單
TOOLS = [search_web, read_webpage, add_research_note, get_research_notes]


# 研究代理
def research_agent(user_request, max_steps=100):
    """
    執行自主研究代理。
    代理必須先收集並驗證研究發現，才能結束。
    """
    plan = create_research_plan(user_request)
    print("\n" + "=" * 60)
    print("RESEARCH PLAN")
    print("=" * 60)
    print(plan)

    # 設定初始消息
    messages = [
        {
            "role": "system",
            "content": (
                "你是一位研究代理。"
                "請使用可用工具調查使用者的需求。"
                "請仔細遵循研究計畫。"
                "首先搜尋相關來源。"
                "閱讀有用的來源後，擷取重要發現，並呼叫 add_research_note 加以記錄。"
                "記錄重要發現後，請使用 verify_finding 判斷證據是否確實支持該發現。"
                "請持續研究，直到研究問題已獲得充分調查。"
                "已驗證的研究發現不得為零。"
                "請勿捏造來源或證據。"
            )
        },
        {
            "role": "user",
            "content": (
                f"Research request:\n{user_request}\n\n"
                f"Research plan:\n{plan}"
            )
        }
    ]

    for step in range(max_steps):

        print(f"\n--- Agent Step {step + 1} ---")

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

        # -------------------------------------------------
        # LLM 沒有要求呼叫工具。
        # 不要立刻將此視為任務已完成。
        # 先檢查是否已有經過驗證的研究發現。
        # -------------------------------------------------

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

    return "代理達到了最大步數，但尚未完成研究。"


# 創建研究計劃
def create_research_plan(user_request):
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位研究規劃助理。"
                    "請根據使用者的研究需求，制定一份簡潔且有順序的研究計畫。"
                    "只回傳編號排列的研究步驟。"
                )
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )

    return response.message.content  # 回傳研究計畫
