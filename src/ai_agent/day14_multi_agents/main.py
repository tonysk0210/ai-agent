from manager import run_manager


def main():
    print("=" * 50)
    print(" MULTI-AGENT AI SYSTEM")
    print("=" * 50)

    task = input("\nEnter your task: ")

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


if __name__ == "__main__":
    main()
