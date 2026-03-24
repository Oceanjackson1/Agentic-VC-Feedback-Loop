"""Vercel Serverless 入口 - 引用 backend/ 完整 FastAPI 应用"""

import os
import sys
from pathlib import Path

# 让 backend/ 目录下的模块可被 import
_backend_dir = str(Path(__file__).resolve().parent.parent / "backend")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# 加载 .env（本地开发用，Vercel 上由环境变量替代）
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# 初始化数据库（首次冷启动时创建表）
from config import settings
if settings.DATABASE_URL:
    try:
        from database import init_db
        init_db()
    except Exception:
        pass

# 直接复用 backend/main.py 中定义的 FastAPI app
from main import app
