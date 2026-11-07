from ..llm import call_llm


# 程式撰寫代理
def write_code(task, research, feedback=""):
    prompt = f"""
        你是一位程式撰寫代理。
        
        請根據任務與研究資料撰寫 Python 程式碼。
        
        任務：
        {task}
        
        研究資料：
        {research}
        
        審查者先前的回饋：
        {feedback}  
        
        如果有提供審查者的回饋，請修正其中指出的問題。
        
        請提供：
            1. 簡短說明
            2. 完整的 Python 程式碼
        """

    response = call_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response
