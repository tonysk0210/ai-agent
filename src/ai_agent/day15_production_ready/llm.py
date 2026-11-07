import time
from openai import OpenAI
from .config import BASE_URL, API_KEY, MODEL, MAX_RETRIES, TIMEOUT
from .logger import logger

# 建立 OpenAI 客戶端
client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=TIMEOUT)


def call_llm(messages):
    # 嘗試多次請求 LLM，直到成功或達到最大重試次數
    for attempt in range(1, MAX_RETRIES + 1):  # attempt 會依序是 1、2、3
        try:
            logger.info(f"LLM request attempt {attempt}")
            # 呼叫 LLM 並取得回應
            # messages = [
            #     {"role": "system", "content": "你是一位樂於助人的助理。"},
            #     {"role": "user", "content": "Python 是什麼？"},
            # ]
            response = client.chat.completions.create(model=MODEL, messages=messages)
            logger.info("LLM request successful")

            return response.choices[0].message.content

        except Exception as e:

            logger.error(f"LLM request failed: {e}")

            if attempt == MAX_RETRIES:
                logger.error("Maximum retry limit reached")
                raise RuntimeError("LLM request failed after "f"{MAX_RETRIES} attempts.")

            # 重試的等待時間
            wait_time = attempt * 2
            logger.info(f"Retrying in {wait_time} seconds")
            time.sleep(wait_time)
    return None
