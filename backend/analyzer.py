"""DeepSeek 分析模块：支持多场景 + 长文本分段 + 可选上下文"""

import json
import logging
import os
from typing import Optional

from openai import OpenAI

from prompts import get_scenario

logger = logging.getLogger(__name__)


# ── JSON 修复与校验 ──────────────────────────────────────────


def _try_repair_json(raw: str) -> str:
    """尝试修复被截断的 JSON（未闭合的字符串/数组/对象）"""
    s = raw.rstrip()
    try:
        json.loads(s)
        return s
    except json.JSONDecodeError:
        pass

    last_complete = s.rfind("}")
    while last_complete > 0:
        candidate = s[:last_complete + 1].rstrip().rstrip(",") + "\n]"
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            last_complete = s.rfind("}", 0, last_complete)

    return raw


def _validate_result(raw: str, scenario_id: str) -> list[dict]:
    """校验返回内容为合法 JSON 数组，并按场景校验结构"""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    raw = _try_repair_json(raw)
    data = json.loads(raw)

    if not isinstance(data, list):
        raise ValueError("模型返回的不是 JSON 数组")

    scenario = get_scenario(scenario_id)

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"第 {i + 1} 项不是对象")
        missing = scenario.REQUIRED_FIELDS - set(item.keys())
        if missing:
            raise ValueError(f"第 {i + 1} 项缺少字段: {missing}")

        # 校验嵌套调整字段
        adj_key = None
        for key in ("required_adjustments", "required_preparation", "follow_up"):
            if key in scenario.REQUIRED_FIELDS:
                adj_key = key
                break

        if adj_key:
            adj = item.get(adj_key)
            if not isinstance(adj, dict):
                raise ValueError(f"第 {i + 1} 项 {adj_key} 必须是对象")
            for k in scenario.REQUIRED_ADJUSTMENT_FIELDS:
                if k not in adj:
                    raise ValueError(f"第 {i + 1} 项 {adj_key} 缺少 {k}")

    return data


# ── 文本分段 ──────────────────────────────────────────

_MAX_INPUT_CHARS = 15000
_OVERLAP_CHARS = 500


def _split_transcript(transcript: str) -> list[str]:
    """将过长的文本按段落边界分段"""
    if len(transcript) <= _MAX_INPUT_CHARS:
        return [transcript]

    chunks = []
    start = 0
    while start < len(transcript):
        end = start + _MAX_INPUT_CHARS
        if end >= len(transcript):
            chunks.append(transcript[start:])
            break
        split_at = transcript.rfind("\n\n", start + _MAX_INPUT_CHARS // 2, end)
        if split_at == -1:
            split_at = transcript.rfind("\n", start + _MAX_INPUT_CHARS // 2, end)
        if split_at == -1:
            split_at = end
        chunks.append(transcript[start:split_at])
        start = max(start + 1, split_at - _OVERLAP_CHARS)

    logger.info(f"文本过长 ({len(transcript)} 字符)，已分为 {len(chunks)} 段处理")
    return chunks


# ── API 调用 ──────────────────────────────────────────


def _call_deepseek(client: OpenAI, prompt: str, scenario_id: str) -> list[dict]:
    """单次 API 调用，含 1 次重试（总共最多 2 次，适配 Vercel 60s 限制）"""
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8192,
            stream=False,
        )
        raw = resp.choices[0].message.content or ""
        finish_reason = resp.choices[0].finish_reason
        if finish_reason == "length":
            logger.warning("模型输出因 token 限制被截断，尝试修复 JSON")
        return _validate_result(raw, scenario_id)
    except (json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"模型返回无法解析: {e}")
    except Exception as e:
        raise RuntimeError(f"API 调用失败: {e}")


# ── 主入口 ──────────────────────────────────────────

_CONTEXT_TEMPLATE = """————————
背景资料（来自用户上传的参考文档）：

{context_text}
"""


def analyze(
    transcript: str,
    scenario_id: str = "vc_pitch",
    output_lang: str = "zh",
    context_text: Optional[str] = None,
) -> list[dict]:
    """
    调用 DeepSeek API 分析 transcript。
    - scenario_id: 场景 ID（vc_pitch / ecommerce_b2b / interview / meeting_summary）
    - output_lang: "zh" 中文 / "en" 英文
    - context_text: 可选的背景资料文本（来自用户上传的上下文 PDF）
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")

    scenario = get_scenario(scenario_id)

    if output_lang == "en":
        lang_instruction = (
            "【重要】文本内容主要为英文。你必须将 JSON 中所有字段的文本值使用英文输出，"
            "包括 evidence_quotes 中的引用也需翻译为英文。"
        )
    else:
        lang_instruction = ""

    context_section = ""
    if context_text and context_text.strip():
        # 限制上下文长度，避免挤占 transcript 空间
        max_context_chars = 30000
        if len(context_text) > max_context_chars:
            context_text = context_text[:max_context_chars] + "\n\n（背景资料过长，已截断）"
            logger.warning(f"上下文文本过长，已截断至 {max_context_chars} 字符")
        context_section = _CONTEXT_TEMPLATE.format(context_text=context_text)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=45.0,
    )

    chunks = _split_transcript(transcript)
    all_results = []

    for i, chunk in enumerate(chunks):
        chunk_note = ""
        if len(chunks) > 1:
            chunk_note = f"\n\n【注意】这是完整文本的第 {i + 1}/{len(chunks)} 段。请只分析本段中出现的问题。\n"
            logger.info(f"正在分析第 {i + 1}/{len(chunks)} 段 ({len(chunk)} 字符)")

        prompt = (
            scenario.ANALYSIS_PROMPT
            .replace("<<<CONTEXT_SECTION>>>", context_section)
            .replace("<<<TRANSCRIPT>>>", chunk_note + chunk)
            .replace("<<<OUTPUT_LANG_INSTRUCTION>>>", lang_instruction)
        )

        results = _call_deepseek(client, prompt, scenario_id)
        all_results.extend(results)

    if not all_results:
        raise RuntimeError("分析结果为空")

    return all_results


# ── 公开接口：供分步 API 调用 ──────────────────────────────────


def split_transcript(transcript: str) -> list[str]:
    """公开的文本分段接口"""
    return _split_transcript(transcript)


def analyze_single_chunk(
    chunk: str,
    chunk_index: int,
    total_chunks: int,
    scenario_id: str,
    output_lang: str = "zh",
    context_text: str | None = None,
) -> list[dict]:
    """分析单个文本块（供分步 API 使用）"""
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")

    scenario = get_scenario(scenario_id)

    lang_instruction = ""
    if output_lang == "en":
        lang_instruction = (
            "【重要】文本内容主要为英文。你必须将 JSON 中所有字段的文本值使用英文输出，"
            "包括 evidence_quotes 中的引用也需翻译为英文。"
        )

    context_section = ""
    if context_text and context_text.strip():
        # 限制上下文长度，避免 prompt 过大导致响应慢
        ctx = context_text[:5000] if len(context_text) > 5000 else context_text
        context_section = _CONTEXT_TEMPLATE.format(context_text=ctx)

    chunk_note = ""
    if total_chunks > 1:
        chunk_note = f"\n\n【注意】这是完整文本的第 {chunk_index + 1}/{total_chunks} 段。请只分析本段中出现的问题。\n"

    prompt = (
        scenario.ANALYSIS_PROMPT
        .replace("<<<CONTEXT_SECTION>>>", context_section)
        .replace("<<<TRANSCRIPT>>>", chunk_note + chunk)
        .replace("<<<OUTPUT_LANG_INSTRUCTION>>>", lang_instruction)
    )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
        timeout=45.0,
    )

    return _call_deepseek(client, prompt, scenario_id)
