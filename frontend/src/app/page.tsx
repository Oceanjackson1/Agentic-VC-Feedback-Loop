"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { GoogleLoginButton } from "@/components/GoogleLoginButton";

const SCENARIOS = [
  { id: "vc_pitch", title: "VC Pitch 反馈", desc: "分析投资人与创始团队的对话，还原投资人问题背后的真实动机，评估团队回答质量，提供下次更优的话术建议。", tag: "适合：创业者、融资团队" },
  { id: "ecommerce_b2b", title: "电商 B2B 对谈", desc: "分析采购方与供应商的订单谈判对话，提取关键诉求，评估应对策略，优化报价话术和跟进方案。", tag: "适合：电商从业者、销售团队" },
  { id: "interview", title: "面试分析", desc: "分析面试官与候选人的对话，识别考察维度，评估回答表现，提供理想回答框架和面试教练建议。", tag: "适合：HR、面试官、求职者" },
  { id: "meeting_summary", title: "会议总结", desc: "结构化会议纪要，提取关键决策、行动项与待跟进事项，自动分配责任人和时间节点。", tag: "适合：团队管理者、项目经理" },
];

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && user) {
      router.push("/dashboard");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-6 h-6 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-bg">
      {/* ── Header ── */}
      <header className="sticky top-0 z-50 bg-bg/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          {/* Left: Logo */}
          <a href="#" onClick={(e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); }} className="flex items-center gap-2 shrink-0">
            <img src="/logo.png" alt="DialogAI" className="h-7 w-7 object-contain" />
            <span className="text-lg font-bold tracking-tight text-text">DialogAI</span>
          </a>
          {/* Center: Nav */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#scenarios" className="text-sm text-text-secondary hover:text-text transition-colors">产品</a>
            <a href="#how" className="text-sm text-text-secondary hover:text-text transition-colors">功能</a>
            <a href="#pricing" className="text-sm text-text-secondary hover:text-text transition-colors">定价</a>
          </nav>
          {/* Right: Actions */}
          <div className="flex items-center gap-3">
            {user ? (
              <button
                onClick={() => router.push("/dashboard")}
                className="px-4 py-1.5 rounded-full bg-text text-bg text-sm font-medium hover:bg-text/90 transition-colors"
              >
                进入看板
              </button>
            ) : (
              <GoogleLoginButton variant="header" />
            )}
          </div>
        </div>
      </header>

      {/* ── Hero ── */}
      <section className="max-w-6xl mx-auto px-6 pt-24 pb-20">
        <p className="text-sm text-accent font-medium mb-4">AI 对话分析</p>
        <h1 className="text-4xl md:text-5xl lg:text-[3.5rem] font-bold leading-[1.15] tracking-tight text-text mb-3">
          把对话变成洞察
        </h1>
        <p className="text-xl md:text-2xl text-text-secondary font-normal leading-relaxed mb-10 max-w-2xl">
          旨在大幅提升您的生产力，是 AI 配合业务的最佳方式。
        </p>
        <GoogleLoginButton variant="hero" />
      </section>

      {/* ── 四大场景 ── */}
      <section id="scenarios" className="max-w-6xl mx-auto px-6 pb-28">
        <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">四大分析场景</h2>
        <p className="text-base text-text-secondary mb-10 max-w-xl">
          针对不同对话类型，AI 提供专业视角的结构化分析。
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {SCENARIOS.map((s) => (
            <div
              key={s.id}
              onClick={() => router.push(`/analyze?scenario=${s.id}`)}
              className="bg-card rounded-2xl p-7 flex flex-col min-h-[180px] cursor-pointer hover:shadow-md transition-all duration-200 group"
            >
              <h3 className="text-base font-semibold mb-2">{s.title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed mb-4">{s.desc}</p>
              <span className="text-accent text-sm font-medium mt-auto group-hover:underline">{s.tag} →</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── 功能介绍 ── */}
      <section id="how" className="max-w-6xl mx-auto px-6 pb-28">
        <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">
          能够完成真实的分析任务
        </h2>
        <p className="text-base text-text-secondary mb-10 max-w-xl">
          上传文件、选择场景，AI 自动生成专业 Excel 分析报告。
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {[
            { title: "上传对话文件", desc: "支持 PDF、Word、TXT 等格式。也可上传背景资料作为分析上下文。", link: "#scenarios" },
            { title: "添加上下文", desc: "可选上传项目 Deck 或公司介绍 PDF，让 AI 基于背景做更精准的分析。", link: "#scenarios" },
            { title: "导出与迭代", desc: "分析结果导出为结构化 Excel，支持中英文输出，帮助团队持续改进。", link: "#pricing" },
          ].map((f) => (
            <div key={f.title} className="bg-card rounded-2xl p-7">
              <h3 className="font-semibold mb-2">{f.title}</h3>
              <p className="text-sm text-text-secondary leading-relaxed mb-4">{f.desc}</p>
              <a href={f.link} className="text-accent text-sm font-medium hover:underline">了解更多 →</a>
            </div>
          ))}
        </div>
      </section>

      {/* ── 定价 ── */}
      <section id="pricing" className="max-w-6xl mx-auto px-6 pb-28">
        <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-2">定价</h2>
        <p className="text-base text-text-secondary mb-10 max-w-xl">
          简单透明的价格，按需选择适合你的方案。
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Free */}
          <div className="bg-card rounded-2xl p-7 flex flex-col">
            <p className="text-xs font-medium text-accent uppercase tracking-wider mb-3">受邀用户</p>
            <div className="flex items-baseline gap-1 mb-1">
              <span className="text-3xl font-bold">免费</span>
            </div>
            <p className="text-sm text-text-secondary mb-6">通过邀请加入的用户可永久免费使用</p>
            <ul className="space-y-2.5 text-sm text-text-secondary mb-8">
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>全部 4 个分析场景</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>上下文 PDF 上传</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>中英文 Excel 导出</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>每日限额分析次数</li>
            </ul>
            <GoogleLoginButton variant="hero" />
          </div>

          {/* Monthly */}
          <div className="bg-card rounded-2xl p-7 flex flex-col ring-2 ring-accent relative">
            <span className="absolute -top-3 left-7 px-3 py-0.5 bg-accent text-white text-xs font-medium rounded-full">推荐</span>
            <p className="text-xs font-medium text-accent uppercase tracking-wider mb-3">月订阅</p>
            <div className="flex items-baseline gap-1 mb-1">
              <span className="text-3xl font-bold">$9.9</span>
              <span className="text-sm text-text-tertiary">/ 月</span>
            </div>
            <p className="text-sm text-text-secondary mb-6">适合个人用户和小团队的日常使用</p>
            <ul className="space-y-2.5 text-sm text-text-secondary mb-8">
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>全部功能无限制</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>不限分析次数</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>优先处理队列</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>分析历史记录</li>
            </ul>
            <button className="w-full py-3 rounded-full bg-text text-bg font-medium text-sm hover:bg-text/90 transition-colors">
              开始订阅
            </button>
          </div>

          {/* Yearly */}
          <div className="bg-card rounded-2xl p-7 flex flex-col">
            <p className="text-xs font-medium text-accent uppercase tracking-wider mb-3">年订阅</p>
            <div className="flex items-baseline gap-1 mb-1">
              <span className="text-3xl font-bold">$99</span>
              <span className="text-sm text-text-tertiary">/ 年</span>
            </div>
            <p className="text-sm text-text-secondary mb-1">相当于 $8.25/月</p>
            <p className="text-xs text-accent font-medium mb-5">节省 17%</p>
            <ul className="space-y-2.5 text-sm text-text-secondary mb-8">
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>月订阅全部权益</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>年度价格锁定</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>团队协作功能（即将推出）</li>
              <li className="flex items-start gap-2"><span className="text-accent mt-0.5">✓</span>专属客户支持</li>
            </ul>
            <button className="w-full py-3 rounded-full bg-text text-bg font-medium text-sm hover:bg-text/90 transition-colors">
              开始订阅
            </button>
          </div>
        </div>
      </section>

      {/* ── Logo Trust Bar ── */}
      <section className="max-w-6xl mx-auto px-6 pb-28">
        <p className="text-center text-sm text-text-tertiary mb-6">深受构建世界一流业务的团队每日信赖</p>
        <div className="grid grid-cols-3 md:grid-cols-9 gap-3">
          {["OKX", "Binance", "Coinbase", "Kraken", "Alibaba", "TikTok", "Figma", "Bybit", "Gate.io"].map((name) => (
            <div key={name} className="bg-card rounded-xl flex items-center justify-center py-4 px-2">
              <span className="text-sm font-bold text-text tracking-tight">{name}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-border">
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
            {/* Brand */}
            <div className="col-span-2 md:col-span-1">
              <span className="flex items-center gap-2 text-lg font-bold text-text">
                <img src="/logo.png" alt="DialogAI" className="h-6 w-6 object-contain" />
                DialogAI
              </span>
              <p className="text-sm text-text-secondary mt-2 leading-relaxed">
                AI 驱动的多场景对话分析平台，帮助团队从每一次对话中获取可执行的洞察。
              </p>
              <p className="text-sm text-text-secondary mt-3">
                开发者：<a href="https://x.com/Ocean_Jackon" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">Ocean</a>
              </p>
            </div>

            {/* 产品 */}
            <div>
              <p className="text-sm font-semibold text-text mb-3">产品</p>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><a href="#scenarios" className="hover:text-text transition-colors">分析场景</a></li>
                <li><a href="#how" className="hover:text-text transition-colors">功能介绍</a></li>
                <li><a href="#pricing" className="hover:text-text transition-colors">定价方案</a></li>
              </ul>
            </div>

            {/* 场景 */}
            <div>
              <p className="text-sm font-semibold text-text mb-3">场景</p>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><a href="#scenarios" className="hover:text-text transition-colors">VC Pitch 反馈</a></li>
                <li><a href="#scenarios" className="hover:text-text transition-colors">电商 B2B 对谈</a></li>
                <li><a href="#scenarios" className="hover:text-text transition-colors">面试分析</a></li>
                <li><a href="#scenarios" className="hover:text-text transition-colors">会议总结</a></li>
              </ul>
            </div>

            {/* 支持 */}
            <div>
              <p className="text-sm font-semibold text-text mb-3">支持</p>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li><a href="https://github.com/Oceanjackson1/Agentic-VC-Feedback-Loop" target="_blank" rel="noopener noreferrer" className="hover:text-text transition-colors">GitHub</a></li>
                <li><a href="https://x.com/Ocean_Jackon" target="_blank" rel="noopener noreferrer" className="hover:text-text transition-colors">联系开发者</a></li>
                <li><span className="hover:text-text transition-colors cursor-pointer">隐私政策</span></li>
                <li><span className="hover:text-text transition-colors cursor-pointer">服务条款</span></li>
              </ul>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="border-t border-border pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-xs text-text-tertiary">© 2024 DialogAI. Built by Ocean.</p>
            <div className="flex items-center gap-5 text-text-tertiary">
              {/* Twitter/X */}
              <a href="https://x.com/Ocean_Jackon" target="_blank" rel="noopener noreferrer" className="hover:text-text transition-colors" title="Twitter / X">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </a>
              {/* GitHub */}
              <a href="https://github.com/Oceanjackson1/Agentic-VC-Feedback-Loop" target="_blank" rel="noopener noreferrer" className="hover:text-text transition-colors" title="GitHub">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
