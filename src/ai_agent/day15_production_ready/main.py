import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_agent.day15_production_ready.agent.manager import run_manager
from ai_agent.day15_production_ready.permissions import demonstrate_permissions


def main():
    print("=" * 50)
    print(" INTELLIGENT MULTI-AGENT SYSTEM")
    print("=" * 50)

    task = input("\nEnter your task: ")

    try:
        state = run_manager(task)
        print("\n" + "=" * 50)
        print(" RESEARCH")
        print("=" * 50)
        # 1. 印出研究結果
        print(state["research"])

        print("\n" + "=" * 50)
        print(" CODE")
        print("=" * 50)
        # 2. 印出程式碼
        print(state["code"])

        print("\n" + "=" * 50)
        print(" REVIEW")
        print("=" * 50)
        # 3. 印出審查結果
        print(state["review"])

        demonstrate_permissions()
    except ValueError as e:
        print(f"\nValidation error: {e}")
    return


if __name__ == "__main__":
    main()
