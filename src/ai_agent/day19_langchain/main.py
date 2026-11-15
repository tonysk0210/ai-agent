from model import model
from prompt import prompt

# 使用 prompt 生成對話模板
messages = prompt.invoke(
    {
        "question": "請用兩個句子說明什麼是 AI agent。"
    }
)

response = model.invoke(messages)
# response = model.invoke("請用兩個句子說明什麼是 AI agent。")

print(response.content)
