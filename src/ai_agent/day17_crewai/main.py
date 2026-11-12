from crew import crew


def main():
    # 1. 啟動 Crew，開始執行任務
    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
