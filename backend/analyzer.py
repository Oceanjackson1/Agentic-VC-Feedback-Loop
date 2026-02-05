"""DeepSeek 分析模块：单次 API 调用完成全部分析"""

import json
import os
from openai import OpenAI

ANALYSIS_PROMPT = """你是一名一线（Tier 1）风险投资机构的投资合伙人，
在 Web2 与 Web3 领域都有长期投资与投后经验，
你经常通过创始团队与投资人的真实交流来判断一个项目是否值得进入下一轮沟通。

现在你将收到一段【完整的文字记录】，内容来自：
- 投资人与初创团队之间的真实交流

你的任务不是复述内容，
而是像一名专业 VC 一样，对这段交流进行结构化拆解和判断。

————————
分析基本定义（必须遵守）：

1. 一个「分析单元」= 投资人提出的一个核心问题
   - 即使问题分散在多句话中
   - 即使包含追问，也视为同一个问题
2. 不构成风险判断的寒暄或肯定性评价可以忽略
3. 判断重点是：团队是否回答了投资人真正关心的核心问题

————————
分析目标：

- 还原投资人问题背后的真实动机
- 判断团队是否有效回应该动机
- 评估表达、结构与叙事质量
- 给出下一次更优的回答方式
- 明确指出产品、叙事或团队准备上的调整方向

————————
输出格式要求（强制）：

你必须只输出一个 JSON 数组，不得输出任何额外文字。

数组中的每一个对象，代表一个投资人提出的核心问题，
并且必须严格符合以下结构：

{
  "question_summary": "一句话总结投资人提出的问题",
  "investor_core_motive": "分析该问题背后的真实关注点或风险判断",
  "team_response_assessment": "评估团队是否回答到位，以及原因",
  "next_time_response_suggestion": "下次更优的回答方式（可直接复述的话术）",
  "delivery_and_pitch_feedback": "从表达方式、结构或话术角度的改进建议",
  "required_adjustments": {
    "product": "产品或业务层面需要调整的地方，没有则写「无」",
    "narrative": "对外叙事或定位需要调整的地方，没有则写「无」",
    "team_preparation": "团队准备或认知层面需要补足的地方，没有则写「无」"
  },
  "evidence_quotes": [
    "用于支撑判断的原文引用，必须直接来自文本"
  ],
  "severity": "high | medium | low"
}

————————
分析原则（必须遵守）：

- 保持专业、审慎、偏投资决策视角
- 避免泛泛而谈的创业建议
- 不要编造文本中不存在的信息
- 如果团队没有回答问题，必须明确指出
- evidence_quotes 必须是真实原文
- severity 表示该问题对投资决策的重要程度

————————
以下是需要分析的文本内容（来自用户上传文件的文本抽取结果）：

<<<TRANSCRIPT>>>
"""


def _validate_result(raw: str) -> list[dict]:
    """校验返回内容为合法 JSON 数组，并校验结构"""
    raw = raw.strip()
    # 去除可能的 markdown 代码块
    if raw.startswith("```"):
        lines = raw.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("模型返回的不是 JSON 数组")
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"第 {i + 1} 项不是对象")
        required = {
            "question_summary", "investor_core_motive", "team_response_assessment",
            "next_time_response_suggestion", "delivery_and_pitch_feedback",
            "required_adjustments", "evidence_quotes", "severity"
        }
        missing = required - set(item.keys())
        if missing:
            raise ValueError(f"第 {i + 1} 项缺少字段: {missing}")
        adj = item.get("required_adjustments")
        if not isinstance(adj, dict):
            raise ValueError(f"第 {i + 1} 项 required_adjustments 必须是对象")
        for k in ("product", "narrative", "team_preparation"):
            if k not in adj:
                raise ValueError(f"第 {i + 1} 项 required_adjustments 缺少 {k}")
    return data


def analyze(transcript: str) -> list[dict]:
    """
    调用 DeepSeek 原生 API 分析 transcript，
    返回结构化的 JSON 数组。校验失败时重试 1 次。
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未配置 DEEPSEEK_API_KEY 环境变量")

    prompt = ANALYSIS_PROMPT.replace("<<<TRANSCRIPT>>>", transcript)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    for attempt in range(2):
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                stream=False,
            )
            raw = resp.choices[0].message.content or ""
            return _validate_result(raw)
        except (json.JSONDecodeError, ValueError) as e:
            if attempt == 1:
                raise RuntimeError(f"模型返回无法解析，已重试 1 次: {e}")
            continue
