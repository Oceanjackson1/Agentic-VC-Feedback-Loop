"""Excel 导出模块：将分析结果导出为 .xlsx"""

from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter


def to_excel(items: list[dict], lang: str = "zh") -> bytes:
    """
    将分析结果 JSON 数组转为 Excel 文件，返回 bytes。
    每一行 = 一个投资人核心问题，列严格对应 JSON 结构。
    lang: "zh" 中文表头与内容，"en" 英文表头与内容
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Investor Q&A Analysis" if lang == "en" else "投资人问题分析"

    headers_zh = [
        "问题摘要 (question_summary)",
        "投资人核心动机 (investor_core_motive)",
        "团队回应评估 (team_response_assessment)",
        "下次更优回答建议 (next_time_response_suggestion)",
        "表达与路演反馈 (delivery_and_pitch_feedback)",
        "产品调整 (required_adjustments.product)",
        "叙事调整 (required_adjustments.narrative)",
        "团队准备调整 (required_adjustments.team_preparation)",
        "证据引用 (evidence_quotes)",
        "重要程度 (severity)",
        "AI建议 (ai_recommendation)",
    ]
    headers_en = [
        "Question Summary",
        "Investor Core Motive",
        "Team Response Assessment",
        "Next-Time Response Suggestion",
        "Delivery & Pitch Feedback",
        "Product Adjustment",
        "Narrative Adjustment",
        "Team Preparation Adjustment",
        "Evidence Quotes",
        "Severity",
        "AI Recommendation",
    ]
    headers = headers_en if lang == "en" else headers_zh
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    # 数据行
    for row_idx, item in enumerate(items, 2):
        adj = item.get("required_adjustments") or {}
        quotes = item.get("evidence_quotes")
        quote_text = "\n".join(quotes) if isinstance(quotes, list) else str(quotes or "")

        row_data = [
            item.get("question_summary", ""),
            item.get("investor_core_motive", ""),
            item.get("team_response_assessment", ""),
            item.get("next_time_response_suggestion", ""),
            item.get("delivery_and_pitch_feedback", ""),
            adj.get("product", ""),
            adj.get("narrative", ""),
            adj.get("team_preparation", ""),
            quote_text,
            item.get("severity", ""),
            item.get("ai_recommendation", ""),
        ]
        for col, val in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col, value=val)
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    # 列宽
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 28

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()
