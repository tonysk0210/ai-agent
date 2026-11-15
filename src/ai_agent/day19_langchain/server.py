from datetime import datetime
import random
import secrets
import string

from fastmcp import FastMCP

# 建立名為 Time Server 的 MCP server。server 檔案裡再用 @mcp.tool() 註冊 current_time 等工具，並呼叫 mcp.run() 開始提供服務。
# "Time Server" 是 server 的名稱
mcp = FastMCP("Time Server")


@mcp.tool()
def current_time():
    """回傳目前的日期與時間。"""
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


@mcp.tool()
def roll_dice():
    """擲出一顆六面骰子。"""
    return random.randint(1, 6)


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
    mcp.run()
