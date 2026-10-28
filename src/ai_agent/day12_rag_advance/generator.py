from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "qwen3:1.7b"


def generate_answer(query, results):
    # 1. 拼接上下文
    # results = [
    #     {"text": "第一段相關內容"},
    #     {"text": "第二段相關內容"}
    # ]

    # 第一段相關內容
    #
    # 第二段相關內容
    context = "\n\n".join(result["text"] for result in results)

    prompt = f"""
        只能根據提供的上下文回答使用者的問題。
        
        上下文：
        {context}
        
        問題：
        {query}
        
        規則：
        
        1. 只能使用提供的上下文。
        2. 不要編造資訊。
        3. 如果上下文中沒有答案，請說明目前沒有相關資訊。
        4. 回答要清楚簡潔。
        """

    # 2. 呼叫 OpenAI API 生成回應
    # ChatCompletion(
    #     id="chatcmpl-...",
    #     model="...",
    #     choices=[
    #         Choice(
    #             index=0,
    #             message=ChatCompletionMessage(
    #                 role="assistant",
    #                 content="模型生成的回答"
    #             ),
    #             finish_reason="stop"
    #         )
    #     ],
    #     usage=...
    # )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()
