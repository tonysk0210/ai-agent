from datetime import datetime
import random
import secrets
import string
from fastmcp import FastMCP  # 快速開發 MCP（Model Context Protocol）伺服器的高階 Python 框架

mcp = FastMCP("Time Server")  # 創建一個 MCP 伺服器，名為 "Time Server"


# 定義一個工具函數，回傳目前的日期和時間；@mcp.tool() 會讓 FastMCP 把函式 docstring 當作工具描述，註冊到 MCP 工具資訊中
@mcp.tool()
def current_time():
    """回傳目前的日期和時間。"""
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


# 定義一個工具函數，擲一顆六面骰子
@mcp.tool()
def roll_dice():
    """擲一顆六面骰子。"""
    return random.randint(1, 6)


# 定義一個工具函數，產生安全的密碼
@mcp.tool()
def generate_password(length: int = 12):
    """
    產生安全的密碼。
    """
    alphabet = (
            string.ascii_letters
            + string.digits
            + string.punctuation
    )
    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


if __name__ == "__main__":
    print("Starting MCP server..")
    mcp.run()  # 開始運行 MCP 伺服器
