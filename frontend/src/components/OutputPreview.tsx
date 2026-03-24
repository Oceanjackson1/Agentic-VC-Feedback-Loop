"use client";

const SCENARIO_OUTPUT: Record<string, { label: string; fields: string[]; desc: string }> = {
  vc_pitch: {
    label: "VC Pitch 反馈",
    desc: "AI 将以 Tier-1 VC 投资合伙人视角，对每一个投资人核心问题进行结构化拆解：",
    fields: [
      "问题摘要 — 投资人提出的核心问题",
      "投资人核心动机 — 问题背后的真实关注点",
      "团队回应评估 — 团队是否回答到位",
      "下次更优回答建议 — 可直接复述的话术",
      "表达与路演反馈 — 结构和话术改进",
      "产品 / 叙事 / 团队调整 — 三维度改进方向",
      "证据引用 — 原文直接引用",
      "重要程度 — High / Medium / Low",
      "AI 建议 — 该问题应在 Pitch / 附录 / Q&A 哪里讲",
    ],
  },
  ecommerce_b2b: {
    label: "电商 B2B 对谈",
    desc: "AI 将以资深 B2B 商务总监视角，对每一个采购方核心关注点进行策略分析：",
    fields: [
      "关注点摘要 — 采购方的核心诉求",
      "采购方真实需求 — 背后的决策考量",
      "供应商回应评估 — 回应是否到位",
      "更优应对建议 — 可直接使用的话术",
      "沟通技巧反馈 — 商务沟通改进建议",
      "价格策略 / 产品服务 / 跟进行动 — 三维度调整",
      "证据引用 — 原文直接引用",
      "重要程度 — High / Medium / Low",
      "成交影响分析 — 对成交概率的影响与建议",
    ],
  },
  interview: {
    label: "面试分析",
    desc: "AI 将以资深 HR 总监和面试教练视角，对每一个考察维度进行评估：",
    fields: [
      "问题摘要 — 面试官的核心问题",
      "考察维度 — 真正考察的能力维度",
      "候选人表现 — 亮点和不足评估",
      "理想回答框架 — 可直接参考的回答结构",
      "改进建议 — 具体提升方向",
      "知识 / 经验 / 表达准备 — 三维度补强",
      "证据引用 — 原文直接引用",
      "重要程度 — High / Medium / Low",
      "教练建议 — 未来面试的综合策略",
    ],
  },
  meeting_summary: {
    label: "会议总结",
    desc: "AI 将以首席幕僚视角，对每一个会议议题进行结构化纪要提炼：",
    fields: [
      "议题摘要 — 核心讨论议题",
      "核心讨论 — 不同观点和关键信息",
      "达成决策 — 明确的决策和结论",
      "行动项 — 谁、做什么、何时完成",
      "待解决问题 — 未解决的分歧",
      "下一步 / 责任人 / 时间节点 — 跟进安排",
      "证据引用 — 原文直接引用",
      "优先级 — High / Medium / Low",
      "管理建议 — 后续会议跟进建议",
    ],
  },
};

interface Props {
  scenario: string;
}

export function OutputPreview({ scenario }: Props) {
  const data = SCENARIO_OUTPUT[scenario] || SCENARIO_OUTPUT.vc_pitch;

  return (
    <div className="rounded-2xl bg-card p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <svg className="w-5 h-5 text-accent" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h7.5c.621 0 1.125-.504 1.125-1.125m-9.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-7.5A1.125 1.125 0 0112 18.375m9.75-12.75c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125m19.5 0v1.5c0 .621-.504 1.125-1.125 1.125M2.25 5.625v1.5c0 .621.504 1.125 1.125 1.125m0 0h17.25m-17.25 0h7.5c.621 0 1.125.504 1.125 1.125M3.375 8.25c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m17.25-3.75h-7.5c-.621 0-1.125.504-1.125 1.125m8.625-1.125c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M12 10.875v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125M13.125 12h7.5m-7.5 0c-.621 0-1.125.504-1.125 1.125M20.625 12c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h7.5M12 14.625v-1.5m0 1.5c0 .621-.504 1.125-1.125 1.125M12 14.625c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m0 0v1.5c0 .621-.504 1.125-1.125 1.125" />
        </svg>
        <h3 className="text-sm font-semibold text-text">分析输出预览</h3>
      </div>

      {/* Scenario badge */}
      <span className="inline-block px-2.5 py-1 rounded-full bg-accent-light text-accent text-xs font-medium mb-3">
        {data.label}
      </span>

      {/* Description */}
      <p className="text-xs text-text-secondary leading-relaxed mb-4">{data.desc}</p>

      {/* Fields list */}
      <ul className="space-y-2 mb-5">
        {data.fields.map((field, i) => {
          const [title, desc] = field.split(" — ");
          return (
            <li key={i} className="flex items-start gap-2.5">
              <span className="text-accent text-xs font-semibold mt-0.5 shrink-0 w-4 text-right">{i + 1}</span>
              <div className="min-w-0">
                <span className="text-xs font-medium text-text">{title}</span>
                {desc && <span className="text-xs text-text-tertiary"> — {desc}</span>}
              </div>
            </li>
          );
        })}
      </ul>

      {/* Export format */}
      <div className="flex items-center gap-2 pt-4 border-t border-border">
        <svg className="w-4 h-4 text-text-tertiary" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        <span className="text-xs text-text-secondary">导出格式：结构化 Excel (.xlsx)</span>
      </div>
    </div>
  );
}
