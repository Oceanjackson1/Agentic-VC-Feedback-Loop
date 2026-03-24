"""分析路由：多场景文件分析 + 可选上下文"""

import logging
from typing import Optional
from urllib.parse import quote

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response

from analyzer import analyze
from extractors import extract_text, ExtractionError
from translator import translate_to_english, translate_to_chinese
from lang_detect import is_primarily_english
from excel_export import to_excel
from prompts import get_scenario

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["analyze"])

# 上下文 PDF 最大字符数
_MAX_CONTEXT_CHARS = 30000


@router.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    scenario: str = Form(...),
    language: str = Form(...),
    context_file: Optional[UploadFile] = File(None),
):
    """
    上传文件 -> 抽取文本 -> 按场景分析 -> 翻译(可选) -> 导出 Excel
    """
    # ── 参数校验 ──
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

    # ── 抽取主文件文本 ──
    try:
        transcript = extract_text(content, file.filename)
    except ExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="该文件无法解析为文本")

    # ── 抽取上下文 PDF（可选）──
    context_text = None
    if context_file and context_file.filename:
        try:
            ctx_content = await context_file.read()
            if ctx_content:
                context_text = extract_text(ctx_content, context_file.filename)
                if context_text and len(context_text) > _MAX_CONTEXT_CHARS:
                    context_text = context_text[:_MAX_CONTEXT_CHARS]
                    logger.warning("上下文文件过长，已截断")
        except ExtractionError:
            logger.warning("上下文文件无法解析，忽略")

    # ── 分析 ──
    is_english_source = is_primarily_english(transcript)
    output_lang = "en" if (language == "en" and is_english_source) else "zh"

    try:
        result = analyze(
            transcript,
            scenario_id=scenario,
            output_lang=output_lang,
            context_text=context_text,
        )
    except Exception as e:
        logger.exception("分析失败")
        raise HTTPException(status_code=500, detail=str(e))

    if not result:
        raise HTTPException(status_code=500, detail="分析结果为空")

    # ── 翻译（需要时）──
    if language == "en" and not is_english_source:
        try:
            result = translate_to_english(result)
        except Exception as e:
            logger.exception("翻译失败")
            raise HTTPException(status_code=500, detail=f"翻译失败: {e}")
    elif language == "zh" and is_english_source:
        try:
            result = translate_to_chinese(result)
        except Exception as e:
            logger.exception("翻译失败")
            raise HTTPException(status_code=500, detail=f"翻译失败: {e}")

    # ── 导出 Excel ──
    try:
        excel_bytes = to_excel(result, lang=language, scenario_id=scenario)
    except Exception as e:
        logger.exception("Excel 导出失败")
        raise HTTPException(status_code=500, detail=f"Excel 导出失败: {e}")

    base = (file.filename or "export").rsplit(".", 1)[0] if "." in (file.filename or "") else (file.filename or "export")
    safe_name = f"{base}_analysis_result.xlsx" if language == "en" else f"{base}_分析结果.xlsx"
    encoded_name = quote(safe_name, safe="")
    disp = f"attachment; filename*=UTF-8''{encoded_name}"

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": disp},
    )
