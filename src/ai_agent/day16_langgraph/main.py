import asyncio

from agent.mcp_client import connect, disconnect, discover_tools
from langgraph.types import Command
from graph import build_graph


async def main():
    # 1. 連接到 MCP 伺服器
    client = await connect()

    try:
        # 2. 從伺服器取得所有工具
        tools = await discover_tools(client)

        print()
        print("Available Tools")
        print("----------------")

        # 3. 列出所有工具
        for tool in tools:
            print(tool.name)

        # 4. 建立 LangGraph
        graph = build_graph(tools, client)

        user_request = input("\nUser : ")

        # 5. 建立 state 初始狀態
        initial_state = {
            "user_request": user_request,
            "current_step": 0,
            "max_steps": 5,
            "actions": [],
            "observations": [],
            "action": "",
            "approval": "",
            "finished": False,
            "final_answer": ""
        }

        # 6. 建立 config 並傳入 thread_id
        # 就 LangGraph 的 checkpointer 設定而言，"configurable" 和 "thread_id" 都是固定欄位名稱，要用這些 key，LangGraph 才能從 config 裡找到執行緒 ID
        # graph.ainvoke(input, config) 的第二個參數必須符合 LangGraph 的執行設定格式 RunnableConfig；在 Python 裡，通常以字典傳入。
        # configurable 用來放執行時要提供給圖的設定；這裡的 thread_id 讓 checkpointer 把這次執行和它的檢查點對應起來。恢復中斷的執行時，也要傳入相同的 config。
        config = {
            "configurable": {"thread_id": "demo-1"}
        }

        # 7. 呼叫 LangGraph 並傳入初始狀態，並回傳最終狀態
        result_state = await graph.ainvoke(initial_state, config)
        # result_state =
        # {
        #     "user_request": "解釋 Python",
        #     "current_step": 0,
        #     "max_steps": 5,
        #     "actions": [],
        #     "observations": [],
        #     "action": "search",
        #     "approval": "",
        #     "finished": False,
        #     "final_answer": "",
        #     "__interrupt__": (
        #         Interrupt(
        #             value={
        #                 "message": "Approve this tool call?",
        #                 "action": "search"
        #             },
        #             ...
        #         ),
        #     )
        # }

        # 8. 如果有中斷，詢問使用者是否同意，並回傳決定給 LangGraph
        while True:
            # 取得中斷資訊，若沒有中斷就跳出迴圈
            # LangGraph 在執行遇到 interrupt() 時，會在回傳的 state 中放入 __interrupt__ 欄位。這行用 .get() 讀取它：有中斷時得到中斷資訊；沒有這個 key 時得到 None。
            interrupts = result_state.get("__interrupt__")
            #     (
            #         Interrupt(
            #             value={
            #                 "message": "Approve this tool call?",
            #                 "action": "search"
            #             },
            #             ...
            #         ),
            #     )

            # 如果沒有中斷，跳出迴圈
            if not interrupts:
                break

            # 因為 interrupts[0] 是 tuple 裡的第一個 Interrupt 物件，而 .value 會取出這個物件的 value 欄位。
            # {
            #     "message": "Approve this tool call?",
            #     "action": "search"
            # }
            interrupt_data = interrupts[0].value

            print("\n==============================")
            print(" HUMAN APPROVAL REQUIRED")
            print("==============================")

            print(interrupt_data["message"])  # "Approve this tool call?"
            print("Tool:", interrupt_data["action"])  # "search"

            decision = input("\nApprove? (yes/no): ").strip().lower()  # "yes" or "no"

            # 呼叫 LangGraph 並傳入決定，並回傳最終狀態
            result_state = await graph.ainvoke(
                Command(resume=decision),  # Command(resume=decision) 會建立一個 Command 物件，並把使用者的決定傳給它。LangGraph 會從這個物件裡讀取 resume 欄位，知道使用者的決定。
                config)
            # **圖再次遇到 interrupt：**回傳包含更新後 state 和 __interrupt__ 的結果。
            # **圖走到 answer 並結束：**回傳最終 state，例如：
            # final result_state =
            # {
            #     "user_request": "解釋 Python",
            #     "current_step": 1,
            #     "max_steps": 5,
            #     "actions": ["search"],
            #     "observations": [...],
            #     "action": "FINISH",
            #     "approval": "yes",
            #     "finished": True,
            #     "final_answer": "..."
            # }

        print("\nFinal State")
        print("-----------")
        print(result_state)  # 印出最終狀態

    finally:
        await disconnect(client)


if __name__ == "__main__":
    asyncio.run(main())
