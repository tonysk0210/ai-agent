import numpy as np  # 載入 numpy 庫，用於數值計算


# 計算向量之間的餘弦相似度
def cosine_similarity(vector1, vector2):
    v1 = np.array(vector1)  # 將向量1轉換為 numpy 陣列
    v2 = np.array(vector2)  # 將向量2轉換為 numpy 陣列

    return np.dot(v1, v2) / (  # 計算向量1和向量2的點積
            np.linalg.norm(v1) *  # 計算向量1的.norm()
            np.linalg.norm(v2)  # 計算向量2的.norm()
    )
