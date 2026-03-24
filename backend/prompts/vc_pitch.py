"""VC Pitch 反馈场景：分析投资人与创始团队的对话"""

SCENARIO_ID = "vc_pitch"

SCENARIO_META = {
    "name_zh": "VC Pitch 反馈",
    "name_en": "VC Pitch Feedback",
    "description_zh": "分析投资人与创始团队的对话，提取核心问题与改进建议",
    "description_en": "Analyze investor-founder conversations for key questions and improvements",
    "icon": "chart-bar",
}

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

<<<CONTEXT_SECTION>>>

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
  "severity": "high | medium | low",
  "ai_recommendation": "基于完整 Pitch + Q&A 的整体判断，说明：该问题应（1）在 Pitch 主线中提前回答、（2）作为 Appendix / Follow-up Material 补充、或（3）仅 Q&A 回答即可；并给出具体改进建议（若提前讲，应在 Pitch 哪个层次；若补充材料，应包含什么关键信息；以及如何更清晰表达）。必须具体可执行，避免泛泛而谈。"
}

————————
分析原则（必须遵守）：

- 保持专业、审慎、偏投资决策视角
- 避免泛泛而谈的创业建议
- 不要编造文本中不存在的信息
- 如果团队没有回答问题，必须明确指出
- evidence_quotes 必须是真实原文
- severity 表示该问题对投资决策的重要程度
- ai_recommendation 为基于完整 Pitch + Q&A 的全局前瞻性建议：判断该问题应「在 Pitch 中提前讲」「作为补充材料」或「仅 Q&A 回答」；并给出具体改进建议。不重复已有分析，而是 Pitch 层面的前瞻性建议。

<<<OUTPUT_LANG_INSTRUCTION>>>

————————
以下是需要分析的文本内容（来自用户上传文件的文本抽取结果）：

<<<TRANSCRIPT>>>
"""

REQUIRED_FIELDS = {
    "question_summary", "investor_core_motive", "team_response_assessment",
    "next_time_response_suggestion", "delivery_and_pitch_feedback",
    "required_adjustments", "evidence_quotes", "severity", "ai_recommendation"
}

REQUIRED_ADJUSTMENT_FIELDS = ("product", "narrative", "team_preparation")

EXCEL_HEADERS_ZH = [
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

EXCEL_HEADERS_EN = [
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

SHEET_NAME_ZH = "投资人问题分析"
SHEET_NAME_EN = "Investor Q&A Analysis"


def extract_row(item: dict) -> list:
    """从分析 JSON 对象提取 Excel 行数据"""
    adj = item.get("required_adjustments") or {}
    quotes = item.get("evidence_quotes")
    quote_text = "\n".join(quotes) if isinstance(quotes, list) else str(quotes or "")
    return [
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
