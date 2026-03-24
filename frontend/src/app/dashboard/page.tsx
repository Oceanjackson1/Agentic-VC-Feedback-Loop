"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { ScenarioCard } from "@/components/ScenarioCard";
import { fetchScenarios, ScenarioMeta } from "@/lib/api";

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [scenarios, setScenarios] = useState<ScenarioMeta[]>([]);

  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [user, loading, router]);

  useEffect(() => {
    fetchScenarios()
      .then(setScenarios)
      .catch(console.error);
  }, []);

  if (loading || !user) return null;

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-bg/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <h1
            className="flex items-center gap-2 text-lg font-bold tracking-tight text-text cursor-pointer"
            onClick={() => router.push("/dashboard")}
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
          {scenarios.map((s) => (
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
