from datetime import datetime
import random
import secrets
import string


def get_current_time():
    """回傳目前的日期和時間。"""
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


def roll_dice():
    """回傳 1 到 6 之間的隨機數字。"""
    return random.randint(1, 6)


def generate_password(length=12):
    """產生安全的隨機密碼。"""
    characters = (
            string.ascii_letters +
            string.digits +
            string.punctuation
    )
    password = ""
    for _ in range(length):
        password += secrets.choice(characters)
    return password


def read_text_file(filename):
    """讀取文字檔案的內容。"""
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "錯誤：找不到檔案。"
