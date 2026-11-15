from agent import research_agent, generate_report
from tools import get_verified_research_notes

request = """
搜尋 AI agent 領域最新的工作職缺，並說明最重要的五項技能要求。
"""

research_agent(request, max_steps=100)

verified_notes = get_verified_research_notes()  # 取得已驗證的研究筆記

# 1. 檢查是否有已驗證的研究筆記
if not verified_notes:
    print("\n目前沒有收集到已驗證的研究發現。")
    raise SystemExit

# 2. 印出已驗證的研究筆記數量
print("\nVerified findings:", len(verified_notes))

# 3. 生成報告
report = generate_report(user_request=request, verified_notes=verified_notes)

print("\n")
print("=" * 60)
print("FINAL RESEARCH REPORT")
print("=" * 60)
print("\n")
print(report)

# 呼叫研究代理
# answer = research_agent(request, max_steps=100)
#
# print("\nFINAL ANSWER\n")
# print(answer)
