import os

from dotenv import load_dotenv

load_dotenv()
from langchain_ollama import ChatOllama

MODEL_NAME = os.getenv("MODEL", "qwen3:1.7b")

# Ollama API 基底位址 (default: http://localhost:11434)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

model = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
