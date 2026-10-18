from datetime import datetime  # 加入日期時間模組
import random  # 加入隨機模組
import secrets  # 加入隨機模組
import string  # 加入字元模組


# 取得當前時間
def get_current_time():
    """回傳目前的日期和時間。"""

    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


# 擲骰子
def roll_dice():
    """回傳 1 到 6 之間的隨機數字。"""

    return random.randint(1, 6)


# 生成密碼
def generate_password(length=12):
    """產生安全的隨機密碼。"""

    # 定義密碼可能包含的字元 abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    characters = (
            string.ascii_letters +
            string.digits +
            string.punctuation
    )

    password = ""

    # 隨機選擇字元
    # - _：迴圈變數，但程式不需要使用它的值。用 _ 表示「這個值我不在意」。
    for _ in range(length):
        password += secrets.choice(characters)  # 從字串 characters 中安全地隨機挑一個字元。

    return password
