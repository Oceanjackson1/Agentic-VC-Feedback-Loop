"""会议总结场景：结构化会议纪要与行动项提取"""

SCENARIO_ID = "meeting_summary"

SCENARIO_META = {
    "name_zh": "会议总结",
    "name_en": "Meeting Summary",
    "description_zh": "结构化会议纪要，提取关键决策、行动项与待跟进事项",
    "description_en": "Generate structured meeting minutes with decisions, action items and follow-ups",
    "icon": "clipboard-list",
}

ANALYSIS_PROMPT = """你是一名资深的企业管理顾问和会议效率专家，
擅长从会议对话中提炼关键信息，生成结构化的会议纪要。

现在你将收到一段【完整的文字记录】，内容来自：
- 团队内部会议、跨部门会议、或外部合作会议

你的任务不是复述内容，
而是像一名专业的首席幕僚一样，将会议内容转化为可执行的结构化纪要。

————————
分析基本定义（必须遵守）：

1. 一个「分析单元」= 会议中讨论的一个核心议题
   - 包括正式议程项和临时提出的重要话题
   - 同一议题的多轮讨论归为同一个单元
2. 纯粹的闲聊和无实质内容的过渡语可以忽略
3. 重点关注：达成了什么决策、分配了什么任务、有什么未解决的问题

————————
分析目标：

- 提炼每个议题的核心讨论内容
- 记录明确的决策和结论
- 提取具体的行动项（谁、做什么、何时完成）
- 识别未解决的问题和分歧
- 标记需要后续跟进的事项

<<<CONTEXT_SECTION>>>

————————
输出格式要求（强制）：

你必须只输出一个 JSON 数组，不得输出任何额外文字。

数组中的每一个对象，代表会议中的一个核心议题，
并且必须严格符合以下结构：

{
  "topic_summary": "一句话总结该议题",
  "discussion_highlights": "核心讨论内容摘要，包含不同观点",
  "decisions_made": "该议题下达成的明确决策，没有则写「无」",
  "action_items": "具体的行动项（含责任人和时间节点），没有则写「无」",
  "open_questions": "未解决的问题或分歧，没有则写「无」",
  "follow_up": {
    "next_steps": "下一步需要做的事情，没有则写「无」",
    "responsible_parties": "相关责任人，没有则写「无」",
    "deadline_or_timeline": "时间节点或截止日期，没有则写「无」"
  },
  "evidence_quotes": [
    "用于支撑判断的原文引用，必须直接来自文本"
  ],
  "priority": "high | medium | low",
  "strategic_note": "从管理视角的补充说明：该议题对团队/项目的影响，以及建议如何在后续会议中跟进"
}

————————
分析原则（必须遵守）：

- 保持中立、客观的记录视角
- 不添加个人评价或偏见
- 不要编造文本中不存在的信息
- 行动项必须尽量具体（谁、做什么、何时）
- evidence_quotes 必须是真实原文
- priority 表示该议题的紧急程度和重要性
- strategic_note 为管理层视角的前瞻性建议

<<<OUTPUT_LANG_INSTRUCTION>>>

————————
以下是需要分析的文本内容（来自用户上传文件的文本抽取结果）：

<<<TRANSCRIPT>>>
"""

REQUIRED_FIELDS = {
    "topic_summary", "discussion_highlights", "decisions_made",
    "action_items", "open_questions",
    "follow_up", "evidence_quotes", "priority", "strategic_note"
}

REQUIRED_ADJUSTMENT_FIELDS = ("next_steps", "responsible_parties", "deadline_or_timeline")

EXCEL_HEADERS_ZH = [
    "议题摘要 (topic_summary)",
    "核心讨论 (discussion_highlights)",
    "达成决策 (decisions_made)",
    "行动项 (action_items)",
    "待解决问题 (open_questions)",
    "下一步 (next_steps)",
    "责任人 (responsible_parties)",
    "时间节点 (deadline_or_timeline)",
    "证据引用 (evidence_quotes)",
    "优先级 (priority)",
    "管理建议 (strategic_note)",
]

EXCEL_HEADERS_EN = [
    "Topic Summary",
    "Discussion Highlights",
    "Decisions Made",
    "Action Items",
    "Open Questions",
    "Next Steps",
    "Responsible Parties",
    "Deadline / Timeline",
    "Evidence Quotes",
    "Priority",
    "Strategic Note",
]

SHEET_NAME_ZH = "会议纪要"
SHEET_NAME_EN = "Meeting Minutes"


def extract_row(item: dict) -> list:
    """从分析 JSON 对象提取 Excel 行数据"""
    fu = item.get("follow_up") or {}
    quotes = item.get("evidence_quotes")
    quote_text = "\n".join(quotes) if isinstance(quotes, list) else str(quotes or "")
    return [
        item.get("topic_summary", ""),
        item.get("discussion_highlights", ""),
        item.get("decisions_made", ""),
        item.get("action_items", ""),
        item.get("open_questions", ""),
        fu.get("next_steps", ""),
        fu.get("responsible_parties", ""),
        fu.get("deadline_or_timeline", ""),
        quote_text,
        item.get("priority", ""),
        item.get("strategic_note", ""),
    ]
