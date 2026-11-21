# 使用精簡版 Python 3.13 映像，與專案要求的 Python 版本一致。
FROM python:3.13-slim

# 設定容器內的工作目錄；後續相對路徑都以 /app 為基準。
WORKDIR /app

# 設定容器環境變數：
# PYTHONDONTWRITEBYTECODE 避免產生 .pyc 檔案。
# PYTHONUNBUFFERED 讓應用程式日誌立即輸出到容器日誌。
# OLLAMA_BASE_URL 指向 Docker Desktop 上的 Windows 主機 Ollama；執行時可覆寫。
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OLLAMA_BASE_URL=http://host.docker.internal:11434

# 先複製相依套件清單；程式碼變動時可沿用已快取的套件安裝層。
COPY src/ai_agent/day20_deployment/requirements.txt .

# 安裝 FastAPI、LangChain、Ollama 等應用程式相依套件，並略過 pip 快取以減少映像大小。
RUN pip install --no-cache-dir -r requirements.txt

# 將 Day 20 FastAPI 應用程式複製到容器內的 /app/Day20。
COPY src/ai_agent/day20_deployment/ /app/Day20/

# 把應用程式目錄設為工作目錄，讓 main:app 可匯入 main.py 裡的 app。
WORKDIR /app/Day20

# 宣告應用程式使用 8000 埠；執行容器時仍需用 -p 對外發布連接埠。
EXPOSE 8000

# 容器啟動時以 Uvicorn 執行 main.py 中的 app，並監聽所有網路介面的 8000 埠。
# 0.0.0.0 表示接受容器所有網路介面的連線；8000 是容器內的埠號。
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 建立 image
# 在包含 Dockerfile 的專案根目錄執行：docker build -t ai-agent-day20 .
# image : - ai-agent-day20:latest：Dockerfile 註解裡的指令 docker build -t ai-agent-day20 . 指定的名稱。latest 是未指定 tag 時 Docker 使用的預設標籤
