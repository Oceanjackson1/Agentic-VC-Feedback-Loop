"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { ScenarioCard } from "@/components/ScenarioCard";
import { ScenarioMeta } from "@/lib/api";

const SCENARIOS: ScenarioMeta[] = [
  { id: "vc_pitch", name_zh: "VC Pitch 反馈", name_en: "VC Pitch Feedback", description_zh: "分析投资人与创始团队的对话，提取核心问题与改进建议", description_en: "Analyze investor-founder conversations for key questions and improvements", icon: "chart-bar" },
  { id: "ecommerce_b2b", name_zh: "电商 B2B 对谈", name_en: "E-commerce B2B", description_zh: "分析采购方与供应商的订单谈判对话，提取关键诉求与改进建议", description_en: "Analyze buyer-supplier negotiations for key demands and improvements", icon: "shopping-cart" },
  { id: "interview", name_zh: "面试分析", name_en: "Interview Analysis", description_zh: "分析面试官与候选人的对话，评估回答质量与改进建议", description_en: "Analyze interviewer-candidate dialogues for response quality and improvements", icon: "user-check" },
  { id: "meeting_summary", name_zh: "会议总结", name_en: "Meeting Summary", description_zh: "结构化会议纪要，提取关键决策、行动项与待跟进事项", description_en: "Generate structured meeting minutes with decisions, action items and follow-ups", icon: "clipboard-list" },
];

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [user, loading, router]);

  if (loading || !user) return null;

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-bg/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <h1
            className="flex items-center gap-2 text-lg font-bold tracking-tight text-text cursor-pointer"
            onClick={() => router.push("/")}
          >
            <img src="/logo.png" alt="DialogAI" className="h-7 w-7 object-contain" />
            DialogAI
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-text-secondary">{user.name || user.email}</span>
            {user.avatar_url && (
              <img
                src={user.avatar_url}
                alt="avatar"
                className="w-8 h-8 rounded-full border border-border"
              />
            )}
            <button
              onClick={() => { logout(); router.push("/"); }}
              className="text-sm text-text-tertiary hover:text-text transition-colors"
            >
              退出
            </button>
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="max-w-5xl mx-auto px-6 py-16">
        <p className="text-sm text-accent font-medium mb-3">开始分析</p>
        <h2 className="text-3xl font-bold tracking-tight mb-2">选择分析场景</h2>
        <p className="text-text-secondary mb-10">选择最匹配你对话内容的场景，AI 将提供针对性的专业分析。</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {SCENARIOS.map((s) => (
            <ScenarioCard
              key={s.id}
              scenario={s}
              onClick={(id) => router.push(`/analyze?scenario=${id}`)}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
