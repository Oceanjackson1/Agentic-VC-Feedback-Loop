"""DeepSeek 翻译模块：分析结果中英互译"""

import json
import os
from openai import OpenAI


def translate_to_english(items: list[dict]) -> list[dict]:
    """
    调用 DeepSeek API 将分析结果 JSON 数组中所有文本字段翻译为英文。
    保持 JSON 结构不变，包括 evidence_quotes 在内的全部文本均翻译为英文。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")

    prompt = f"""你是一个专业翻译。请将以下 JSON 数组中的所有文本内容翻译为英文。
要求：
1. 保持 JSON 结构完全不变
2. 仅翻译各字段的文本值，不要修改字段名（key）
3. severity 保持 "high" | "medium" | "low" 不变
4. evidence_quotes 中的引用也必须翻译为英文
5. 翻译要专业、准确，符合 VC/创业领域术语

输入 JSON：
```json
{json.dumps(items, ensure_ascii=False, indent=2)}
```

只输出翻译后的完整 JSON 数组，不要输出任何其他文字。"""

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    raw = resp.choices[0].message.content or ""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)
    return json.loads(raw)


def translate_to_chinese(items: list[dict]) -> list[dict]:
    """
    调用 DeepSeek API 将分析结果 JSON 数组中所有文本字段翻译为中文。
    用于原文为英文、用户选择中文 Excel 输出的场景。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")

    prompt = f"""你是一个专业翻译。请将以下 JSON 数组中的所有文本内容翻译为中文。
要求：
1. 保持 JSON 结构完全不变
2. 仅翻译各字段的文本值，不要修改字段名（key）
3. severity 保持 "high" | "medium" | "low" 不变
4. evidence_quotes 中的引用必须翻译为中文
5. 翻译要专业、准确，符合 VC/创业领域术语

输入 JSON：
```json
{json.dumps(items, ensure_ascii=False, indent=2)}
```

只输出翻译后的完整 JSON 数组，不要输出任何其他文字。"""

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    raw = resp.choices[0].message.content or ""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)
    return json.loads(raw)
