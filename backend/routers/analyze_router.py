"""分析路由：多场景文件分析 - 支持分步处理长文本"""

import logging
from typing import Optional
from urllib.parse import quote

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from analyzer import analyze, split_transcript, analyze_single_chunk
from extractors import extract_text, ExtractionError
from translator import translate_to_english, translate_to_chinese
from lang_detect import is_primarily_english
from excel_export import to_excel
from prompts import get_scenario

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["analyze"])

_MAX_CONTEXT_CHARS = 30000


# ── 分步接口：Step 1 - 提取文本并分段 ──


@router.post("/extract")
async def extract_and_split(
    file: UploadFile = File(...),
    scenario: str = Form(...),
    language: str = Form(...),
    context_file: Optional[UploadFile] = File(None),
):
    """上传文件 → 提取文本 → 返回分段结果"""
    if language not in ("zh", "en"):
        raise HTTPException(status_code=400, detail="请选择输出语言：zh 或 en")

    try:
        get_scenario(scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

    # 上下文
    context_text = None
    if context_file and context_file.filename:
        try:
            ctx_content = await context_file.read()
            if ctx_content:
                context_text = extract_text(ctx_content, context_file.filename)
                if context_text and len(context_text) > _MAX_CONTEXT_CHARS:
                    context_text = context_text[:_MAX_CONTEXT_CHARS]
        except ExtractionError:
            logger.warning("上下文文件无法解析，忽略")

    is_english_source = is_primarily_english(transcript)
    output_lang = "en" if (language == "en" and is_english_source) else "zh"
    chunks = split_transcript(transcript)

    return {
        "chunks": chunks,
        "total_chunks": len(chunks),
        "is_english_source": is_english_source,
        "context_text": context_text,
        "output_lang": output_lang,
    }


# ── 分步接口：Step 2 - 分析单个文本块 ──


class AnalyzeChunkRequest(BaseModel):
    chunk: str
    chunk_index: int
    total_chunks: int
    scenario: str
    output_lang: str
    context_text: Optional[str] = None


@router.post("/analyze-chunk")
async def analyze_chunk(req: AnalyzeChunkRequest):
    """分析单个文本块"""
    try:
        get_scenario(req.scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        results = analyze_single_chunk(
            chunk=req.chunk,
            chunk_index=req.chunk_index,
            total_chunks=req.total_chunks,
            scenario_id=req.scenario,
            output_lang=req.output_lang,
            context_text=req.context_text,
        )
    except Exception as e:
        logger.exception(f"分析第 {req.chunk_index + 1} 段失败")
        raise HTTPException(status_code=500, detail=str(e))

    return {"chunk_index": req.chunk_index, "results": results}


# ── 分步接口：Step 3 - 翻译 + 导出 Excel ──


class ExportRequest(BaseModel):
    results: list[dict]
    language: str
    scenario: str
    is_english_source: bool
    filename: str


@router.post("/export")
async def export_excel(req: ExportRequest):
    """翻译（如需要）并导出 Excel"""
    result = req.results

    if req.language == "en" and not req.is_english_source:
        try:
            result = translate_to_english(result)
        except Exception as e:
            logger.exception("翻译失败")
            raise HTTPException(status_code=500, detail=f"翻译失败: {e}")
    elif req.language == "zh" and req.is_english_source:
        try:
            result = translate_to_chinese(result)
        except Exception as e:
            logger.exception("翻译失败")
            raise HTTPException(status_code=500, detail=f"翻译失败: {e}")

    try:
        excel_bytes = to_excel(result, lang=req.language, scenario_id=req.scenario)
    except Exception as e:
        logger.exception("Excel 导出失败")
        raise HTTPException(status_code=500, detail=f"Excel 导出失败: {e}")

    base = req.filename.rsplit(".", 1)[0] if "." in req.filename else req.filename
    safe_name = f"{base}_analysis_result.xlsx" if req.language == "en" else f"{base}_分析结果.xlsx"
    encoded_name = quote(safe_name, safe="")

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"},
    )


# ── 旧接口（保留兼容）──


@router.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    scenario: str = Form(...),
    language: str = Form(...),
    context_file: Optional[UploadFile] = File(None),
):
    """旧版一体化接口（适用于短文本）"""
    if language not in ("zh", "en"):
        raise HTTPException(status_code=400, detail="请选择输出语言：zh 或 en")

    try:
        get_scenario(scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

    context_text = None
    if context_file and context_file.filename:
        try:
            ctx_content = await context_file.read()
            if ctx_content:
                context_text = extract_text(ctx_content, context_file.filename)
                if context_text and len(context_text) > _MAX_CONTEXT_CHARS:
                    context_text = context_text[:_MAX_CONTEXT_CHARS]
        except ExtractionError:
            pass

    is_english_source = is_primarily_english(transcript)
    output_lang = "en" if (language == "en" and is_english_source) else "zh"

    try:
        result = analyze(transcript, scenario_id=scenario, output_lang=output_lang, context_text=context_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if language == "en" and not is_english_source:
        result = translate_to_english(result)
    elif language == "zh" and is_english_source:
        result = translate_to_chinese(result)

    excel_bytes = to_excel(result, lang=language, scenario_id=scenario)
    base = (file.filename or "export").rsplit(".", 1)[0] if "." in (file.filename or "") else (file.filename or "export")
    safe_name = f"{base}_analysis_result.xlsx" if language == "en" else f"{base}_分析结果.xlsx"
    encoded_name = quote(safe_name, safe="")

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"},
    )
