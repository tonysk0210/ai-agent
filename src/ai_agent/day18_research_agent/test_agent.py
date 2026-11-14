from agent import research_agent

request = """
搜尋 AI agent 領域最新的工作職缺，並說明最重要的五項技能要求。
"""

# 呼叫研究代理
answer = research_agent(request, max_steps=100)

print("\nFINAL ANSWER\n")
print(answer)
