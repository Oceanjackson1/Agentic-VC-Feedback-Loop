"use client";

import { useEffect, useState, useRef, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { AudioGuidePanel } from "@/components/AudioGuidePanel";
import { OutputPreview } from "@/components/OutputPreview";
import { analyzeFile } from "@/lib/api";

function AnalyzeContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { user, loading } = useAuth();

  const scenario = searchParams.get("scenario") || "vc_pitch";

  const [file, setFile] = useState<File | null>(null);
  const [contextFile, setContextFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<"zh" | "en">("zh");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const ctxRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!loading && !user) router.push("/");
  }, [user, loading, router]);

  const SCENARIO_NAMES: Record<string, string> = {
    vc_pitch: "VC Pitch 反馈",
    ecommerce_b2b: "电商 B2B 对谈",
    interview: "面试分析",
    meeting_summary: "会议总结",
  };

  const handleSubmit = async () => {
    if (!file) return;
    setStatus("loading");
    setMessage(language === "en" ? "正在分析并翻译，请稍候..." : "正在分析，请稍候...");

    try {
      const blob = await analyzeFile(file, scenario, language, contextFile);
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      const baseName = file.name.replace(/\.[^.]+$/, "") || "export";
      a.download = language === "en" ? `${baseName}_analysis_result.xlsx` : `${baseName}_分析结果.xlsx`;
      a.click();
      URL.revokeObjectURL(a.href);
      setStatus("success");
      setMessage("分析完成，Excel 已下载");
    } catch (e: unknown) {
      setStatus("error");
      setMessage(e instanceof Error ? e.message : "请求失败，请稍后重试");
    }
  };

  if (loading || !user) return null;

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-bg/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push("/dashboard")}
              className="text-text-tertiary hover:text-text transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <h1 className="text-lg font-semibold">{SCENARIO_NAMES[scenario] || scenario}</h1>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-text-secondary">{user.name || user.email}</span>
          </div>
        </div>
      </header>

      {/* Main — Two Column Layout */}
      <main className="max-w-6xl mx-auto px-6 pt-14 pb-10">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">

          {/* ── Left Column: Controls ── */}
          <div className="lg:col-span-3 space-y-6">
            {/* File Upload Card */}
            <div className="rounded-2xl bg-surface shadow-sm overflow-hidden">
              <div
                className={`p-8 text-center cursor-pointer relative border-2 border-dashed rounded-xl m-5
                           transition-all duration-200 ${
                             dragOver
                               ? "border-accent bg-accent-light"
                               : "border-border-strong hover:border-accent hover:bg-accent-light"
                           }`}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragOver(false);
                  const f = e.dataTransfer.files[0];
                  if (f) setFile(f);
                }}
                onClick={() => fileRef.current?.click()}
              >
                <input
                  ref={fileRef}
                  type="file"
                  className="hidden"
                  accept=".txt,.md,.pdf,.docx,.html,.htm"
                  onChange={(e) => { if (e.target.files?.[0]) setFile(e.target.files[0]); }}
                />
                <svg className="w-12 h-12 mx-auto mb-3 text-text-tertiary" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
                <p className="text-sm font-medium text-text">点击或拖拽文件到此处</p>
                <p className="text-xs text-text-tertiary mt-1">支持 .txt .md .pdf .docx .html</p>
                {file && (
                  <p className="text-xs text-accent font-medium mt-3">已选择: {file.name}</p>
                )}
              </div>

              {/* Context PDF */}
              <div className="px-5 pb-3">
                <div
                  className="flex items-center gap-3 p-3 rounded-xl border border-dashed border-border-strong hover:border-accent
                             cursor-pointer transition-colors"
                  onClick={() => ctxRef.current?.click()}
                >
                  <input
                    ref={ctxRef}
                    type="file"
                    className="hidden"
                    accept=".pdf,.txt,.docx"
                    onChange={(e) => { if (e.target.files?.[0]) setContextFile(e.target.files[0]); }}
                  />
                  <svg className="w-5 h-5 text-text-tertiary shrink-0" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                  </svg>
                  <div className="flex-1 min-w-0">
                    {contextFile ? (
                      <p className="text-sm text-accent truncate">{contextFile.name}</p>
                    ) : (
                      <>
                        <p className="text-sm text-text-secondary">上传背景资料（可选）</p>
                        <p className="text-xs text-text-tertiary">如项目 Deck、公司介绍等</p>
                      </>
                    )}
                  </div>
                  {contextFile && (
                    <button
                      onClick={(e) => { e.stopPropagation(); setContextFile(null); }}
                      className="text-text-tertiary hover:text-error transition-colors"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  )}
                </div>
              </div>

              {/* Language */}
              <div className="px-5 pb-5">
                <p className="text-xs font-medium text-text-secondary mb-2">输出语言</p>
                <div className="flex gap-3">
                  {(["zh", "en"] as const).map((lang) => (
                    <button
                      key={lang}
                      onClick={() => setLanguage(lang)}
                      className={`flex-1 py-2.5 rounded-xl text-sm font-medium transition-all duration-200
                        ${language === lang
                          ? "bg-accent-light border-2 border-accent text-accent"
                          : "bg-card border-2 border-transparent text-text-secondary hover:bg-bg-secondary"
                        }`}
                    >
                      {lang === "zh" ? "中文" : "English"}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Submit */}
            <button
              onClick={handleSubmit}
              disabled={!file || status === "loading"}
              className="w-full py-3.5 rounded-full font-semibold text-sm transition-all duration-200
                         bg-text text-bg hover:bg-text/90
                         disabled:opacity-30 disabled:cursor-not-allowed
                         hover:shadow-md"
            >
              {status === "loading" ? "分析中..." : "开始分析"}
            </button>

            {/* Status */}
            {status !== "idle" && (
              <div
                className={`p-4 rounded-xl text-sm font-medium flex items-center gap-3
                  ${status === "loading" ? "bg-card text-text-secondary" : ""}
                  ${status === "success" ? "bg-success-light text-success" : ""}
                  ${status === "error" ? "bg-error-light text-error" : ""}
                `}
              >
                {status === "loading" && (
                  <div className="w-4 h-4 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow shrink-0" />
                )}
                {message}
              </div>
            )}
          </div>

          {/* ── Right Column: Preview ── */}
          <div className="lg:col-span-2 space-y-6">
            <OutputPreview scenario={scenario} />
          </div>

        </div>

        {/* 录音转文本引导 — 全宽底部 */}
        <div className="mt-8">
          <AudioGuidePanel />
        </div>
      </main>
    </div>
  );
}

export default function AnalyzePage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-bg">
          <div className="w-6 h-6 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow" />
        </div>
      }
    >
      <AnalyzeContent />
    </Suspense>
  );
}
