from langchain.agents import create_agent

from model import model
from tools import current_time, roll_dice, generate_password

# 建立代理機器人
agent = create_agent(
    model=model,
    tools=[
        current_time,
        roll_dice,
        generate_password
    ]
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current time?"
            }
        ]
    }
)

print(result["messages"][-1].content)
print("=" * 50)
print(result)
# {
#     "messages": [
#         # [步驟 1] 使用者提問
#         HumanMessage(
#             content="What is the current time?",
#             id="eab43c5d-c09e-4362-a0a6-231553c9aac1",
#         ),
#         # [步驟 2] 模型判斷需要呼叫外部工具（content 為空，改為發出 tool_calls）
#         AIMessage(
#             content="",
#             id="lc_run--01a1dee2-4924-76b9-8921-750f0a4422fb-0",
#             tool_calls=[
#                 {
#                     "name": "current_time",
#                     "args": {},
#                     "id": "319b2d32-678a-4ece-9e2e-f43f6d3b9fc3",
#                     "type": "tool_call",
#                 }
#             ],
#             response_metadata={"model": "qwen3:1.7b", "model_provider": "ollama", ...},
#             usage_metadata={"input_tokens": 213, "output_tokens": 89, "total_tokens": 302},
#         ),
#         # [步驟 3] LangGraph 的 ToolNode 執行函式，將結果包裝成 ToolMessage 回傳
#         ToolMessage(
#             content="15-11-2026 19:05:37",
#             name="current_time",
#             id="184b655d-7410-4a75-aca1-75babe632b8c",
#             tool_call_id="319b2d32-678a-4ece-9e2e-f43f6d3b9fc3",
#         ),
#         # [步驟 4] 模型讀取到 ToolMessage 後，整理出給人類看的最終回答
#         AIMessage(
#             content="The current time is **15 November 2026 at 19:05:37**. Let me know if you need further assistance!",
#             id="lc_run--01a1dee2-5690-772c-b0e3-c3ec0fca4702-0",
#             tool_calls=[],
#             response_metadata={"model": "qwen3:1.7b", "model_provider": "ollama", ...},
#             usage_metadata={"input_tokens": 261, "output_tokens": 174, "total_tokens": 435},
#         ),
#     ]
# }