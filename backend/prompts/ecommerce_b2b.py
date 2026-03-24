"""电商 B2B 对谈场景：分析采购/订单谈判对话"""

SCENARIO_ID = "ecommerce_b2b"

SCENARIO_META = {
    "name_zh": "电商 B2B 对谈",
    "name_en": "E-commerce B2B",
    "description_zh": "分析采购方与供应商的订单谈判对话，提取关键诉求与改进建议",
    "description_en": "Analyze buyer-supplier negotiations for key demands and improvements",
    "icon": "shopping-cart",
}

ANALYSIS_PROMPT = """你是一名拥有 10 年以上 B2B 电商经验的资深商务总监，
熟悉跨境贸易、大宗采购、供应链谈判等全流程，
你经常通过分析采购方与供应商的真实对话来优化谈判策略和成交率。

现在你将收到一段【完整的文字记录】，内容来自：
- 采购方（买家）与供应商（卖家）之间的真实商务对话

你的任务不是复述内容，
而是像一名专业商务顾问一样，对这段对话进行结构化拆解和策略分析。

————————
分析基本定义（必须遵守）：

1. 一个「分析单元」= 采购方提出的一个核心关注点或需求
   - 包括价格、交期、品质、售后、付款条件等
   - 即使分散在多处讨论，归为同一个关注点
2. 纯粹的客套和无实质内容的寒暄可以忽略
3. 判断重点是：供应商是否有效回应了采购方的核心诉求

————————
分析目标：

- 还原采购方关注点背后的真实需求和决策考量
- 判断供应商是否有效回应该需求
- 评估商务沟通的专业度和说服力
- 给出更优的应对策略和话术
- 指出产品、价格策略或服务层面的改进方向

<<<CONTEXT_SECTION>>>

————————
输出格式要求（强制）：

你必须只输出一个 JSON 数组，不得输出任何额外文字。

数组中的每一个对象，代表采购方的一个核心关注点，
并且必须严格符合以下结构：

{
  "concern_summary": "一句话总结采购方的核心关注点",
  "buyer_real_need": "分析该关注点背后的真实需求或决策考量",
  "supplier_response_assessment": "评估供应商的回应是否到位，以及原因",
  "better_response_suggestion": "更优的应对方式（可直接使用的话术）",
  "communication_feedback": "从商务沟通技巧角度的改进建议",
  "required_adjustments": {
    "pricing_strategy": "价格或报价策略需要调整的地方，没有则写「无」",
    "product_service": "产品或服务层面需要调整的地方，没有则写「无」",
    "follow_up_action": "后续跟进需要做的具体行动，没有则写「无」"
  },
  "evidence_quotes": [
    "用于支撑判断的原文引用，必须直接来自文本"
  ],
  "severity": "high | medium | low",
  "deal_impact": "对成交概率的影响分析，以及建议在后续沟通中如何主动处理此问题"
}

————————
分析原则（必须遵守）：

- 保持商业视角，关注成交转化和长期客户关系
- 避免泛泛而谈的销售建议
- 不要编造文本中不存在的信息
- 如果供应商没有回应某个关注点，必须明确指出
- evidence_quotes 必须是真实原文
- severity 表示该关注点对成交决策的重要程度
- deal_impact 为对整体交易的前瞻性建议

<<<OUTPUT_LANG_INSTRUCTION>>>

————————
以下是需要分析的文本内容（来自用户上传文件的文本抽取结果）：

<<<TRANSCRIPT>>>
"""

REQUIRED_FIELDS = {
    "concern_summary", "buyer_real_need", "supplier_response_assessment",
    "better_response_suggestion", "communication_feedback",
    "required_adjustments", "evidence_quotes", "severity", "deal_impact"
}

REQUIRED_ADJUSTMENT_FIELDS = ("pricing_strategy", "product_service", "follow_up_action")

EXCEL_HEADERS_ZH = [
    "关注点摘要 (concern_summary)",
    "采购方真实需求 (buyer_real_need)",
    "供应商回应评估 (supplier_response_assessment)",
    "更优应对建议 (better_response_suggestion)",
    "沟通技巧反馈 (communication_feedback)",
    "价格策略调整 (pricing_strategy)",
    "产品服务调整 (product_service)",
    "后续跟进行动 (follow_up_action)",
    "证据引用 (evidence_quotes)",
    "重要程度 (severity)",
    "成交影响分析 (deal_impact)",
]

EXCEL_HEADERS_EN = [
    "Concern Summary",
    "Buyer Real Need",
    "Supplier Response Assessment",
    "Better Response Suggestion",
    "Communication Feedback",
    "Pricing Strategy Adjustment",
    "Product/Service Adjustment",
    "Follow-up Action",
    "Evidence Quotes",
    "Severity",
    "Deal Impact Analysis",
]

SHEET_NAME_ZH = "B2B 对谈分析"
SHEET_NAME_EN = "B2B Negotiation Analysis"


def extract_row(item: dict) -> list:
    """从分析 JSON 对象提取 Excel 行数据"""
    adj = item.get("required_adjustments") or {}
    quotes = item.get("evidence_quotes")
    quote_text = "\n".join(quotes) if isinstance(quotes, list) else str(quotes or "")
    return [
        item.get("concern_summary", ""),
        item.get("buyer_real_need", ""),
        item.get("supplier_response_assessment", ""),
        item.get("better_response_suggestion", ""),
        item.get("communication_feedback", ""),
        adj.get("pricing_strategy", ""),
        adj.get("product_service", ""),
        adj.get("follow_up_action", ""),
        quote_text,
        item.get("severity", ""),
        item.get("deal_impact", ""),
    ]
