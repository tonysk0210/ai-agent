import logging

# 這裡設置了基本的日誌配置，指定了日誌級別和輸出格式
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

# 創建一個名為 "agent" 的日誌記錄器
logger = logging.getLogger("agent")
