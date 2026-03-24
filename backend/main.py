"""多场景对话分析平台 - 后端 API"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from routers.analyze_router import router as analyze_router
from routers.scenario_router import router as scenario_router
from routers.auth_router import router as auth_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="多场景对话分析平台")

# 静态文件：frontend 放在 backend 同级
_frontend = Path(__file__).resolve().parent.parent / "frontend"

# CORS：开发时允许所有，生产环境应限制为 Vercel 域名
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(analyze_router)
app.include_router(scenario_router)


@app.get("/")
def root():
    index_path = _frontend / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"status": "ok", "message": "多场景对话分析平台 API"}


@app.get("/health")
def health():
    return {"status": "ok", "version": "v2-railway-300s"}
