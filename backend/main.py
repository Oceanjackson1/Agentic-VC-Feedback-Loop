"""投资人对话总结 Agent - 后端 API"""

import logging
import os
from urllib.parse import quote
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse

from extractors import extract_text, ExtractionError
from analyzer import analyze
from excel_export import to_excel


app = FastAPI(title="投资人对话总结 Agent")

# 静态文件：frontend 放在 backend 同级
_frontend = Path(__file__).resolve().parent.parent / "frontend"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    index_path = _frontend / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"status": "ok", "message": "投资人对话总结 Agent API"}


@app.get("/health")
def health():
    return {"status": "ok"}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/analyze")
async def analyze_file(file: UploadFile):
    """
    上传文件 -> 抽取文本 -> DeepSeek 分析 -> 导出 Excel -> 返回下载
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="未提供文件名")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="文件为空")

    try:
        transcript = extract_text(content, file.filename)
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="该文件无法解析为文本")

    try:
        result = analyze(transcript)
    except Exception as e:
        logger.exception("分析失败")
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=500, detail="分析结果为空")

    try:
        excel_bytes = to_excel(result)
    except Exception as e:
        logger.exception("Excel 导出失败")
        raise HTTPException(status_code=500, detail=f"Excel 导出失败: {e}")
    base = (file.filename or "export").rsplit(".", 1)[0] if "." in (file.filename or "") else (file.filename or "export")
    safe_name = f"{base}_分析结果.xlsx"
    encoded_name = quote(safe_name, safe="")
    # HTTP 头只允许 Latin-1，中文必须用 filename*=UTF-8'' 形式
    disp = f"attachment; filename*=UTF-8''{encoded_name}"

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": disp},
    )
