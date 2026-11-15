from langchain_core.tools import tool
from datetime import datetime
import random
import secrets
import string


@tool
def current_time() -> str:
    """回傳目前的日期與時間。"""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


@tool
def roll_dice() -> int:
    """擲出一顆六面骰子。"""
    return random.randint(1, 6)


@tool
def generate_password(length: int = 12) -> str:
    """產生隨機密碼。"""
    characters = (
            string.ascii_letters
            + string.digits
            + "!@#$%^&*"
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )
