from ..llm import call_llm
from ..validation import validate_task
from ..logger import logger
from ..workers.research_agent import research
from ..workers.coding_agent import write_code
from ..workers.reviewer_agent import review
from .state import create_state
from ..config import MAX_REVISIONS


def choose_worker(state):
    prompt = f"""
            你是管理代理。

            你的工作是決定下一個應該採取行動的代理。

            原始任務：
            {state["task"]}

            研究內容：
            {state["research"]}

            程式碼：
            {state["code"]}

            審查結果：
            {state["review"]}

            執行紀錄：
            {state["history"]}

            修訂次數：
            {state["revision_count"]}

            修訂次數上限：
            {MAX_REVISIONS}

            可用的代理：

            research
            coding
            review
            finish

            決策規則：

            - 如果研究內容是空的，選擇 research。

            - 如果已有研究內容但程式碼是空的，選擇 coding。

            - 如果已有審查結果且狀態為 "needs_revision" 且修訂次數未達上限，選擇 coding。

            - 如果已有程式碼但還沒有審查結果，選擇 review。

            - 如果先前的審查要求修正，且已產生新的程式碼，再次選擇 review。

            - 如果最新審查狀態為 "approved"，選擇 finish。

            - 如果已達修訂次數上限，選擇 finish。

            只回傳一個單字：

            research
            coding
            review
            finish
            """

    response = call_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # 這裡假設 LLM 回傳的內容是單字 "research"、"coding"、"review" 或 "finish"，並且沒有多餘的空白或換行。
    result = response.strip().lower()
    return result


# result =
# "research"
# "coding"
# "review"
# "finish"

# 這是一個管理代理，它的角色是決定下一個應該採取行動的代理。
def run_manager(task):
    # 驗證任務是否為空字串，如果是，則拋出 ValueError。
    task = validate_task(task)
    state = create_state(task)
    # state = {
    #     "task": task,             # 任務內容，通常是字串
    #     "research": "",           # 研究結果，初始為空字串
    #     "code": "",               # 產生的程式碼，初始為空字串
    #     "review": "",             # 審查結果，初始為空字串
    #     "history": [],             # 已執行的代理名稱，list
    #     "revision_count": 0        # 修訂次數，整數
    # }
    logger.info(f"Starting manager for task: {task}")

    while True:

        worker = choose_worker(state)  # 選擇下一個要執行的代理
        print(f"\nManager selected: {worker}")
        logger.info(f"\nManager selected: {worker}")
        # worker =
        # "research"
        # "coding"
        # "review"
        # "finish"

        if worker == "research":

            state["research"] = research(state["task"])
            state["history"].append("research")  # 研究完成
            # []                                      # 剛開始
            # ["research"]                            # 研究完成
            # ["research", "coding"]                  # 程式碼完成
            # ["research", "coding", "review"]        # 審查完成

        elif worker == "coding":

            # 如果已有審查結果且修訂次數已達上限，則中斷迴圈
            if state["review"] and state["revision_count"] >= MAX_REVISIONS:
                print("Maximum revisions reached.")
                logger.warn("Maximum revisions reached: {MAX_REVISIONS}")
                break

            # 取得審查結果中的回饋，如果沒有則回傳空字串
            feedback = ""
            if state["review"]:
                feedback = state["review"].get("feedback", "")  # 取得審查結果中的回饋，如果沒有則回傳空字串

            state["code"] = write_code(state["task"], state["research"], feedback)  # 把回饋 feedback 加入程式碼生成
            state["history"].append("coding")

        elif worker == "review":

            state["review"] = review(state["task"], state["code"])
            state["history"].append("review")  # 審查完成

        elif worker == "finish":
            logger.info("Manager finished the workflow.")
            break
        else:
            raise ValueError(f"Unknown worker: {worker}")

    return state

# 當 research、coding、review 都執行完成後，choose_worker(state) 會選擇 finish，run_manager() 跳出迴圈並回傳 state。最終結構預期如下：
# {
#     "task": "使用者交辦的任務",
#     "research": "研究代理產生的內容",
#     "code": "程式撰寫代理產生的程式碼",
#     "review": {
#         "status": "approved",
#         "feedback": "解答正確。"
#     },
#     "history": ["research", "coding", "review"]
# }
