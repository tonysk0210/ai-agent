from model import model

# 1. 建立訊息清單
messages = [
    {
        "role": "user",
        "content": "My name is Anthony."
    }
]

first_response = model.invoke(messages)

# 2. 將第一個回應加入訊息清單
messages.append(
    {
        "role": "assistant",
        "content": first_response.content
    }
)

# 3. 將第二個問題加入訊息清單
messages.append(
    {
        "role": "user",
        "content": "What is my name?"
    }
)

second_response = model.invoke(messages)

print(second_response.content)
# You're Anthony! I'm glad to meet you. 😊 Let me know if there's anything else I can help with! 🌟
