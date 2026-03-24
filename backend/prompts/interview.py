"""面试分析场景：分析面试官与候选人的对话"""

SCENARIO_ID = "interview"

SCENARIO_META = {
    "name_zh": "面试分析",
    "name_en": "Interview Analysis",
    "description_zh": "分析面试官与候选人的对话，评估回答质量与改进建议",
    "description_en": "Analyze interviewer-candidate dialogues for response quality and improvements",
    "icon": "user-check",
}

ANALYSIS_PROMPT = """你是一名拥有丰富招聘经验的资深 HR 总监和面试教练，
在科技、金融、消费等行业有过大量面试评估经验，
你擅长从面试对话中识别候选人的真实能力水平和潜力。

现在你将收到一段【完整的文字记录】，内容来自：
- 面试官与候选人之间的真实面试对话

你的任务不是复述内容，
而是像一名专业面试评估专家一样，对这段面试进行结构化拆解和评估。

————————
分析基本定义（必须遵守）：

1. 一个「分析单元」= 面试官提出的一个核心问题或考察维度
   - 包括技术能力、行为面试、情景模拟、文化匹配等
   - 追问和补充问题归入同一个考察维度
2. 纯粹的开场寒暄和结束语可以忽略
3. 判断重点是：候选人是否充分展现了该维度的能力

————————
分析目标：

- 还原面试官每个问题真正想考察的能力维度
- 评估候选人的回答是否充分展示了该能力
- 识别回答中的亮点和不足
- 提供更优的回答策略和框架
- 指出候选人需要补强的知识或经验领域

<<<CONTEXT_SECTION>>>

————————
输出格式要求（强制）：

你必须只输出一个 JSON 数组，不得输出任何额外文字。

数组中的每一个对象，代表面试官的一个核心考察问题，
并且必须严格符合以下结构：

{
  "question_summary": "一句话总结面试官的问题",
  "assessment_dimension": "该问题真正考察的能力维度（如领导力、技术深度、问题解决等）",
  "candidate_performance": "评估候选人的表现，包括亮点和不足",
  "ideal_response_framework": "更优的回答框架和策略（可直接参考的结构）",
  "improvement_suggestions": "具体的改进建议，帮助候选人提升表现",
  "required_preparation": {
    "knowledge": "知识层面需要补强的地方，没有则写「无」",
    "experience": "经验或案例层面需要准备的地方，没有则写「无」",
    "presentation": "表达或呈现方式需要调整的地方，没有则写「无」"
  },
  "evidence_quotes": [
    "用于支撑判断的原文引用，必须直接来自文本"
  ],
  "severity": "high | medium | low",
  "coaching_advice": "面试教练视角的综合建议：该问题在面试中的权重判断，以及如何在未来面试中主动展现该维度的能力"
}

————————
分析原则（必须遵守）：

- 保持客观、专业的评估视角
- 避免泛泛而谈的面试技巧
- 不要编造文本中不存在的信息
- 如果候选人没有回答某个问题，必须明确指出
- evidence_quotes 必须是真实原文
- severity 表示该问题对面试结果的影响程度
- coaching_advice 为综合面试策略建议

<<<OUTPUT_LANG_INSTRUCTION>>>

————————
以下是需要分析的文本内容（来自用户上传文件的文本抽取结果）：

<<<TRANSCRIPT>>>
"""

REQUIRED_FIELDS = {
    "question_summary", "assessment_dimension", "candidate_performance",
    "ideal_response_framework", "improvement_suggestions",
    "required_preparation", "evidence_quotes", "severity", "coaching_advice"
}

REQUIRED_ADJUSTMENT_FIELDS = ("knowledge", "experience", "presentation")

EXCEL_HEADERS_ZH = [
    "问题摘要 (question_summary)",
    "考察维度 (assessment_dimension)",
    "候选人表现 (candidate_performance)",
    "理想回答框架 (ideal_response_framework)",
    "改进建议 (improvement_suggestions)",
    "知识补强 (knowledge)",
    "经验准备 (experience)",
    "表达调整 (presentation)",
    "证据引用 (evidence_quotes)",
    "重要程度 (severity)",
    "教练建议 (coaching_advice)",
]

EXCEL_HEADERS_EN = [
    "Question Summary",
    "Assessment Dimension",
    "Candidate Performance",
    "Ideal Response Framework",
    "Improvement Suggestions",
    "Knowledge Preparation",
    "Experience Preparation",
    "Presentation Adjustment",
    "Evidence Quotes",
    "Severity",
    "Coaching Advice",
]

SHEET_NAME_ZH = "面试分析"
SHEET_NAME_EN = "Interview Analysis"


def extract_row(item: dict) -> list:
    """从分析 JSON 对象提取 Excel 行数据"""
    prep = item.get("required_preparation") or {}
    quotes = item.get("evidence_quotes")
    quote_text = "\n".join(quotes) if isinstance(quotes, list) else str(quotes or "")
    return [
        item.get("question_summary", ""),
        item.get("assessment_dimension", ""),
        item.get("candidate_performance", ""),
        item.get("ideal_response_framework", ""),
        item.get("improvement_suggestions", ""),
        prep.get("knowledge", ""),
        prep.get("experience", ""),
        prep.get("presentation", ""),
        quote_text,
        item.get("severity", ""),
        item.get("coaching_advice", ""),
    ]
