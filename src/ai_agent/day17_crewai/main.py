from crew import crew, memory_crew


def main():
    # 1. 啟動 Crew，開始執行任務
    result = crew.kickoff()
    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)
    print("\n")
    print("=" * 60)

    print("DEMO 2: CREWAI MEMORY")
    print("=" * 60)
    # 2. 啟動 Memory Crew，開始執行記憶任務
    memory_result = memory_crew.kickoff()
    print("\n")
    print("MEMORY RESULT")
    print("=" * 60)
    print(memory_result)


if __name__ == "__main__":
    main()
