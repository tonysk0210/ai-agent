# from research_agent import research
# from coding_agent import write_code
# from reviewer_agent import review

# 代理管理員
# def run_manager(task):
#     print("\nManager → Research Agent")
#     research_result = research(task)
#
#     print("\nManager → Coding Agent")
#     code_result = write_code(task, research_result)
#
#     print("\nManager → Reviewer Agent")
#     review_result = review(task, code_result)
#
#     return {
#         "research": research_result,
#         "code": code_result,
#         "review": review_result
#     }

from openai import OpenAI
from dotenv import load_dotenv
import os

from research_agent import research
from coding_agent import write_code
from reviewer_agent import review
from state import create_state

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

MAX_REVISIONS = 3


# 管理代理的主要功能是根據目前的狀態，決定下一個要執行工作的代理。它不會親自執行任務，也不會解釋推理或產生程式碼、研究內容或審查結果。
def choose_worker(state):
    # prompt = f"""
    #     你是多代理系統中的管理代理。
    #
    #     你的唯一職責是根據目前狀態，決定下一個要執行工作的代理。
    #
    #     不要親自執行任務。
    #     不要解釋你的推理。
    #     不要產生程式碼。
    #     不要產生研究內容。
    #     不要審查任何內容。
    #
    #     ========================
    #     原始任務
    #     ========================
    #     {state["task"]}
    #
    #     ========================
    #     目前狀態
    #     ========================
    #
    #     研究內容：
    #     {state["research"]}
    #
    #     程式碼：
    #     {state["code"]}
    #
    #     審查結果：
    #     {state["review"]}
    #
    #     執行紀錄：
    #     {state["history"]}
    #
    #     ========================
    #     可用動作
    #     ========================
    #
    #     research
    #     coding
    #     review
    #     finish
    #
    #     ========================
    #     決策規則
    #     ========================
    #
    #     請嚴格依照以下順序遵守這些規則：
    #
    #     1. 如果研究內容是空的：
    #        回傳 research
    #
    #     2. 否則，如果程式碼是空的：
    #        回傳 coding
    #
    #     3. 否則，如果審查結果是空的：
    #        回傳 review
    #
    #     4. 否則：
    #        回傳 finish
    #
    #     重要事項：
    #     - 如果研究內容已存在，絕不可選擇 research。
    #     - 如果程式碼已存在，絕不可選擇 coding。
    #     - 如果審查結果已存在，絕不可選擇 review。
    #     - 如果研究內容、程式碼或審查結果有任何一項是空的，絕不可選擇 finish。
    #     - 判斷欄位是否完成時，不要考慮欄位中的內容，只檢查欄位是空的還是非空的。
    #     - 執行紀錄僅供參考。目前狀態的優先順序較高。
    #
    #     ========================
    #     輸出格式
    #     ========================
    #
    #     只回傳一個單字。
    #
    #     有效的輸出只有：
    #
    #     research
    #     coding
    #     review
    #     finish
    #
    #     請勿回傳：
    #     - 解釋
    #     - 句子
    #     - Markdown
    #     - 反引號
    #     - 標點符號
    #     - 其他文字
    #
    #     範例：
    #     review
    #     """

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

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip().lower()
    return result


# result =
# "research"
# "coding"
# "review"
# "finish"


def run_manager(task):
    state = create_state(task)
    # state = {
    #     "task": "寫一個計算機",
    #     "research": "",
    #     "code": "",
    #     "review": "",
    #     "history": []
    # }

    while True:

        worker = choose_worker(state)  # 選擇下一個要執行的代理
        print(f"\nManager selected: {worker}")
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
