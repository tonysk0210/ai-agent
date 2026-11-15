from ollama import chat
from tools import search_web, read_webpage, add_research_note, get_research_notes, verify_finding, get_verified_research_notes

MODEL = "qwen3:1.7b"

# 可用的工具函數
AVAILABLE_TOOLS = {
    "search_web": search_web,
    "read_webpage": read_webpage,
    "add_research_note": add_research_note,
    "get_research_notes": get_research_notes,
    "verify_finding": verify_finding
}

# 可用的工具函數清單
TOOLS = [search_web, read_webpage, add_research_note, get_research_notes, verify_finding]


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
                f"研究需求：\n{user_request}\n\n"
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

            # verify_finding():
            # messages = [
            #     {"role": "user", "content": "請研究 AI agents"},
            #
            #     # 模型要求呼叫工具
            #     Message(
            #         role="assistant",
            #         content="",
            #         tool_calls=[
            #             ToolCall(
            #                 function=Function(
            #                     name="verify_finding",
            #                     arguments={
            #                         "source": "https://example.com/article",
            #                         "finding": "AI agents 可以使用工具",
            #                         "evidence": "文章指出代理可以呼叫外部工具。"
            #                     }
            #                 )
            #             )
            #         ]
            #     ),
            #
            #     # verify_finding() 的回傳結果
            #     {
            #         "role": "tool",
            #         "content": "{'supported': True, 'explanation': '證據支持這項研究發現。'}",
            #         "tool_name": "verify_finding"
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
    # "1. 搜尋相關來源\n2. 閱讀並整理證據\n3. 驗證研究發現"


# 產生研究報告
def generate_report(user_request, verified_notes):
    """
    根據已驗證的研究發現產生研究報告。
    """
    # verified_notes =
    # [
    #     {
    #         "source": "https://example.com/article",
    #         "finding": "AI agents 可以使用工具",
    #         "evidence": "文章指出代理可以呼叫外部工具。",
    #         "verified": True,
    #     }
    # ]

    # 將已驗證的研究發現格式化為字串
    research_text = "\n\n".join(
        [
            (
                f"來源：{note['source']}\n"
                f"發現：{note['finding']}\n"
                f"證據：{note['evidence']}"
            )
            for note in verified_notes
        ]
    )
    # research_text =
    # 來源：https://example.com/article
    # 發現：AI agents 可以使用工具
    # 證據：文章指出代理可以呼叫外部工具。
    #
    # 來源：https://example.org/paper
    # 發現：工具呼叫能擴充代理能力
    # 證據：研究描述了代理如何呼叫外部工具。

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的研究報告撰寫者。"
                    "請撰寫一份清楚且結構完整的報告，內容只能使用提供的已驗證的研究發現。"
                    "不得捏造事實或來源。"
                    "如果現有研究資料不足以撰寫某個章節，請明確說明。"
                )
            },
            {
                "role": "user",
                "content": (
                    f"研究需求：\n"
                    f"{user_request}\n\n"
                    f"已驗證的研究發現：\n"
                    f"{research_text}\n\n"
                    "請依照以下章節"
                    "撰寫報告：\n"
                    
                    "1. 執行摘要\n"
                    "2. 緒論\n"
                    "3. 主要發現\n"
                    "4. 分析\n"
                    "5. 研究限制\n"
                    "6. 結論\n"
                    "7. 來源\n\n"
                    "請列出已驗證研究發現中"
                    "使用的來源。"
                    "不得自行編造研究發現中"
                    "未提供的 URL。"
                )
            }
        ]
    )

    return response.message.content
