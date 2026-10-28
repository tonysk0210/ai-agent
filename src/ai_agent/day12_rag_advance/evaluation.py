def evaluate_retrieval(result_chunks, expected_chunk_id):
    # 1. 從結果中提取小塊編號 [2, 0]
    # results = [
    #     {"chunk_id": 2, "text": "..." },
    #     {"chunk_id": 0, "text": "..." }
    # ]
    retrieved_ids = [
        result["chunk_id"]
        for result in result_chunks
    ]

    # 2. 檢查預期的小塊編號是否在提取的小塊編號中 boolean: true / false
    return expected_chunk_id in retrieved_ids
