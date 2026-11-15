from langchain_mcp_adapters.client import MultiServerMCPClient

# 建立一個 MultiServerMCPClient，並登記一個名為 time_server 的 MCP server 連線設定 (adaptor for langchain to mcp server)
# 設定怎麼連接這個 server。"time_server" 是 client 內的連線名稱；command 和 args 指示 client 用 python server.py 啟動 server 子程序；stdio 表示雙方透過標準輸入與標準輸出通訊。
# "time_server" 是 client 設定這條連線時使用的名稱
client = MultiServerMCPClient(
    {
        "time_server": {  # 這個 server 在 client 設定中的名稱。
            "transport": "stdio",
            "command": "python",  # 要啟動的執行程式
            "args": [
                "server.py"
            ]
        }
    }
)
