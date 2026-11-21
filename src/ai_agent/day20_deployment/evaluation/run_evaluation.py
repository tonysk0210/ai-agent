import asyncio
from agent_evaluation import create_agent_instance
from test_cases import test_cases
from evaluate import check_tool


async def main():
    # 1. 這一步是準備 agent，還沒有送出測試問題或要求模型作答
    agent = await create_agent_instance()

    for test_case in test_cases:
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": test_case["question"]
                    }
                ]
            }
        )

        passed = check_tool(result, test_case["expected_tool"])

        print(test_case["question"])

        print("Expected tool:", test_case["expected_tool"])

        print("Tool selection:", "PASS" if passed else "FAIL")

        print()


if __name__ == "__main__":
    asyncio.run(main())
