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
def research_agent(user_request, max_steps=100, progress_callback=None):
    """
    執行自主研究代理。
    代理必須先收集並驗證研究發現，才能結束。
    """

    # 輸出訊息
    # message = {
    #     "type": "plan",
    #     "message": "Research plan created",
    #     "plan": (
    #         "1. 搜尋相關職缺資料\n"
    #         "2. 閱讀來源網頁並整理技能要求\n"
    #         "3. 使用來源證據驗證研究發現"
    #     )
    # }
    # {
    #     "type": "step",
    #     "step": 1,
    #     "message": "Agent step 1"
    # }
    # {
    #     "type": "tool",
    #     "tool": "search_web",
    #     "message": "Using tool: search_web"
    # }
    # {
    #     "type": "verification",
    #     "message": "Verifying research evidence"
    # }
    # {
    #     "type": "tool_complete",
    #     "tool": "verify_finding",
    #     "message": "Completed: verify_finding"
    # }
    # 用於傳送目前狀態給到瀏覽器：progress_callback 會是一個函數
    def emit(message):
        if progress_callback:
            progress_callback(message)

    plan = create_research_plan(user_request)
    print("\n" + "=" * 60)
    print("RESEARCH PLAN")
    print("=" * 60)
    print(plan)

    # I. 輸出研究計劃
    emit({
        "type": "plan",
        "message": "Research plan created",
        "plan": plan
    })

    # 設定初始消息
    messages = [
        {
            "role": "system",
            "content": (
                "你是研究代理。必須使用工具完成研究，不可只根據自身知識回答。\n"
                "請依序執行以下流程，每次只處理一個來源：\n"
                "1. 呼叫 search_web 搜尋職缺資料。\n"
                "2. 對搜尋結果呼叫 read_webpage，閱讀來源原文。\n"
                "3. 從原文擷取一項具體技能要求，保留可支持該要求的原文證據。\n"
                "4. 立即呼叫 add_research_note，提供 source、finding、evidence 三個參數。\n"
                "5. 接著呼叫 verify_finding，使用完全相同的 source 和 finding，並提供 evidence。\n"
                "6. 確認驗證結果 supported 為 true 後，再研究下一項。\n"
                "請重複以上流程，直到取得五項已驗證的不同技能要求。\n"
                "如果證據不足或驗證結果為 false，不能把該項算入五項；請搜尋其他來源。\n"
                "只有五項都已驗證後才能產生最終回答。不得捏造來源或證據。"
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

        # II. 輸出當前步驟
        emit({
            "type": "step",
            "step": step + 1,
            "message": (f"Agent step {step + 1}")
        })

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
            print("\n未呼叫工具，正在處理最終答案。")
            verified_notes = (get_verified_research_notes())
            # verified_notes =[
            #     {
            #         "source": "https://example.com/article",
            #         "finding": "AI agents 可以使用工具",
            #         "evidence": "文章指出代理可以呼叫外部工具。",
            #         "verified": True,
            #     }
            # ]
            if verified_notes:
                print("\n研究完成。")
                print("已收集的驗證研究發現數量：", len(verified_notes))
                return response.message.content
            else:
                print("\n代理嘗試在沒有已驗證研究發現的情況下結束。")
                print("繼續研究...")
                messages.append({
                    "role": "user",
                    "content": (
                        "你嘗試在尚未收集任何已驗證研究發現時結束。"
                        "你現在必須再執行一項研究操作。"
                        "不要提供最終答案。"
                        "請從以下操作中選擇一項：\n"
                        "1. 呼叫 search_web 尋找其他來源。\n"
                        "2. 呼叫 read_webpage 閱讀來源內容。\n"
                        "3. 從來源擷取一項研究發現後，呼叫 add_research_note。\n"
                        "4. 儲存研究發現後，呼叫 verify_finding。\n"
                        "你下一次回覆必須呼叫一個工具。"
                    )
                })
            continue

        # -------------------------------------------------
        # 執行模型要求呼叫的所有工具。
        # -------------------------------------------------

        # 如果有工具呼叫
        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name  # 取得工具名稱
            arguments = tool_call.function.arguments  # 取得工具參數

            print(f"\nCalling tool: {tool_name}")
            print(f"Arguments: {arguments}")

            # III. 輸出工具名稱
            emit({
                "type": "tool",
                "tool": tool_name,
                "message": f"Using tool: {tool_name}"
            })

            # IV. 輸出驗證發現
            if tool_name == "verify_finding":
                emit({
                    "type": "verification",
                    "message": "Verifying research evidence"
                })

            tool_function = AVAILABLE_TOOLS.get(tool_name)  # 取得工具函數 search_web / read_webpage / ...

            # 如果工具函數不存在
            if tool_function is None:
                result = f"Unknown tool: {tool_name}"
            else:
                try:
                    result = tool_function(**arguments)  # 呼叫工具函數
                    # 其中 **arguments 會把字典展開成關鍵字參數，等同於：
                    # result = search_web(query="AI agents", max_results=3)

                    # V. 輸出工具完成訊息
                    emit({
                        "type": "tool_complete",
                        "tool": tool_name,
                        "message": f"Completed: {tool_name}"
                    })
                except Exception as e:
                    result = {
                        "status": "error",
                        "tool": tool_name,
                        "error": str(e)
                    }
                    print(f"Tool error: {e}")
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_name": tool_name
            })
            # messages = [
            #     {
            #         "role": "system",
            #         "content": "研究代理的規則……"
            #     },
            #     {
            #         "role": "user",
            #         "content": "研究需求：Python 工程師職缺需要哪些技能？"
            #     },
            #     Message(  # 一個 assistant Message，裡面有兩筆 ToolCall
            #         role="assistant",
            #         content="",
            #         tool_calls=[
            #             ToolCall(
            #                 function=Function(
            #                     name="search_web",
            #                     arguments={"query": "Python 工程師職缺技能"}
            #                 )
            #             ),
            #             ToolCall(
            #                 function=Function(
            #                     name="read_webpage",
            #                     arguments={"url": "https://example.com/job"}
            #                 )
            #             )
            #         ]
            #     ),
            #     {
            #         "role": "tool",
            #         "content": "[{'title': 'Python 工程師職缺', 'url': 'https://example.com/job'}]",
            #         "tool_name": "search_web"
            #     },
            #     {
            #         "role": "tool",
            #         "content": "網頁內容：職缺要求熟悉 Python……",
            #         "tool_name": "read_webpage"
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
                "content": "你是一位研究分析師。請使用清晰的 Markdown（標題與項目符號）撰寫簡潔、專業的研究報告。"
            },
            {
                "role": "user",
                "content": f"研究主題：{user_request}\n\n已驗證的研究發現：\n{research_text}\n\n請撰寫一份結構清晰的 Markdown 報告。"
            }
        ]
    )

    return response.message.content


# 執行代理：包含 research_agent 及 generate_report
# request = "研究 AI agents 如何使用工具，以及工具呼叫對代理能力的影響。" String
def run_agent(request):
    # 1. 更新 tools.py 裡的 research_notes
    # research_notes = [
    #     {
    #         "source": "https://example.com/job",
    #         "finding": "職缺要求具備 Python 技能",
    #         "evidence": "熟悉 Python 程式設計及相關框架",
    #         "verified": True,
    #     },
    #     {
    #         "source": "https://example.com/article",
    #         "finding": "文章提出的另一項研究發現",
    #         "evidence": "尚未確認是否足以支持該發現的文字",
    #         "verified": False,
    #     },
    # ]
    research_agent(request, max_steps=100)

    # 2. 取得已驗證的研究發現
    # verified_notes = [
    #     {
    #         "source": "https://example.com/job",
    #         "finding": "職缺要求具備 Python 技能",
    #         "evidence": "熟悉 Python 程式設計及相關框架",
    #         "verified": True,
    #     }
    # ]
    verified_notes = (get_verified_research_notes())

    if not verified_notes:
        print("\n未收集到已驗證的研究發現。")
        raise Exception("未收集到已驗證的研究發現。")

    print("\n已驗證的研究發現數量：", len(verified_notes))

    # 3. 產生研究報告
    # 1. 執行摘要
    # ...
    # 
    # 2. 緒論
    # ...
    #
    # 3. 主要發現
    # ...
    #
    # 4. 分析
    # ...
    #
    # 5. 研究限制
    # ...
    #
    # 6. 結論
    # ...
    #
    # 7. 來源
    # ...
    report = generate_report(user_request=request, verified_notes=verified_notes)

    print("\n")
    print("=" * 60)
    print("FINAL RESEARCH REPORT")
    print("=" * 60)
    print("\n")
    print(report)
    return report
