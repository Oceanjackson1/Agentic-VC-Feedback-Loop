"use client";

import { useEffect, useState, useRef, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { AudioGuidePanel } from "@/components/AudioGuidePanel";
import { OutputPreview } from "@/components/OutputPreview";
import { extractFile, analyzeChunk, exportExcel } from "@/lib/api";

type ProgressStep = "idle" | "extracting" | "analyzing" | "exporting" | "done" | "error";

interface Progress {
  step: ProgressStep;
  chunksTotal: number;
  chunksCompleted: number;
  message: string;
}

const STEP_LABELS: Record<ProgressStep, string> = {
  idle: "",
  extracting: "正在提取文本...",
  analyzing: "正在分析",
  exporting: "正在生成 Excel...",
  done: "分析完成，Excel 已下载",
  error: "",
};

function AnalyzeContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { user, loading } = useAuth();

  const scenario = searchParams.get("scenario") || "vc_pitch";

  const [file, setFile] = useState<File | null>(null);
  const [contextFile, setContextFile] = useState<File | null>(null);
  const [language, setLanguage] = useState<"zh" | "en">("zh");
  const [progress, setProgress] = useState<Progress>({
    step: "idle", chunksTotal: 0, chunksCompleted: 0, message: "",
  });
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const ctxRef = useRef<HTMLInputElement>(null);
  const abortRef = useRef(false);

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
    abortRef.current = false;

    try {
      // Step 1: Extract
      setProgress({ step: "extracting", chunksTotal: 0, chunksCompleted: 0, message: "正在提取文本..." });
      const extracted = await extractFile(file, scenario, language, contextFile);

      if (abortRef.current) return;

      // Step 2: Analyze chunks one by one
      const { chunks, total_chunks, is_english_source, context_text, output_lang } = extracted;
      setProgress({ step: "analyzing", chunksTotal: total_chunks, chunksCompleted: 0, message: `正在分析 0/${total_chunks}...` });

      const allResults: Record<string, unknown>[] = [];
      const failedChunks: number[] = [];

      for (let i = 0; i < chunks.length; i++) {
        if (abortRef.current) return;

        setProgress(prev => ({
          ...prev,
          chunksCompleted: i,
          message: `正在分析第 ${i + 1}/${total_chunks} 段...`,
        }));

        try {
          const result = await analyzeChunk({
            chunk: chunks[i],
            chunk_index: i,
            total_chunks,
            scenario,
            output_lang,
            context_text: context_text ? context_text.slice(0, 5000) : null,
          });
          allResults.push(...result.results);
        } catch (e) {
          console.warn(`Chunk ${i} failed:`, e);
          failedChunks.push(i);
        }

        setProgress(prev => ({
          ...prev,
          chunksCompleted: i + 1,
          message: failedChunks.includes(i)
            ? `第 ${i + 1} 段分析失败，继续处理...`
            : `已完成 ${i + 1}/${total_chunks} 段`,
        }));
      }

      if (allResults.length === 0) {
        setProgress({ step: "error", chunksTotal: total_chunks, chunksCompleted: total_chunks, message: "所有段落分析失败，请稍后重试" });
        return;
      }

      if (abortRef.current) return;

      // Step 3: Export
      setProgress(prev => ({ ...prev, step: "exporting", message: "正在生成 Excel..." }));
      const blob = await exportExcel({
        results: allResults,
        language,
        scenario,
        is_english_source,
        filename: file.name,
      });

      // Download
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      const baseName = file.name.replace(/\.[^.]+$/, "") || "export";
      a.download = language === "en" ? `${baseName}_analysis_result.xlsx` : `${baseName}_分析结果.xlsx`;
      a.click();
      URL.revokeObjectURL(a.href);

      const warning = failedChunks.length > 0
        ? `（${failedChunks.length} 段分析失败，结果可能不完整）`
        : "";
      setProgress(prev => ({
        ...prev,
        step: "done",
        message: `分析完成，Excel 已下载${warning}`,
      }));

    } catch (e: unknown) {
      setProgress(prev => ({
        ...prev,
        step: "error",
        message: e instanceof Error ? e.message : "请求失败，请稍后重试",
      }));
    }
  };

  const isProcessing = ["extracting", "analyzing", "exporting"].includes(progress.step);
  const progressPercent = progress.chunksTotal > 0
    ? Math.round((progress.chunksCompleted / progress.chunksTotal) * 100)
    : 0;

  if (loading || !user) return null;

  return (
    <div className="min-h-screen bg-bg">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-bg/80 backdrop-blur-xl border-b border-border">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1
              className="flex items-center gap-2 text-lg font-bold tracking-tight text-text cursor-pointer shrink-0"
              onClick={() => router.push("/")}
            >
              <img src="/logo.png" alt="DialogAI" className="h-7 w-7 object-contain" />
              DialogAI
            </h1>
            <span className="text-border-strong">/</span>
            <button
              onClick={() => router.push("/dashboard")}
              className="text-sm text-text-secondary hover:text-text transition-colors"
            >
              看板
            </button>
            <span className="text-border-strong">/</span>
            <span className="text-sm font-medium text-text">{SCENARIO_NAMES[scenario] || scenario}</span>
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
              onClick={isProcessing ? () => { abortRef.current = true; } : handleSubmit}
              disabled={!file && !isProcessing}
              className={`w-full py-3.5 rounded-full font-semibold text-sm transition-all duration-200
                         ${isProcessing
                           ? "bg-error/10 text-error hover:bg-error/20 border border-error/30"
                           : "bg-text text-bg hover:bg-text/90 hover:shadow-md"
                         }
                         disabled:opacity-30 disabled:cursor-not-allowed`}
            >
              {isProcessing ? "取消分析" : "开始分析"}
            </button>

            {/* Progress */}
            {progress.step !== "idle" && (
              <div
                className={`p-4 rounded-xl text-sm font-medium space-y-3
                  ${isProcessing ? "bg-card text-text-secondary" : ""}
                  ${progress.step === "done" ? "bg-success-light text-success" : ""}
                  ${progress.step === "error" ? "bg-error-light text-error" : ""}
                `}
              >
                <div className="flex items-center gap-3">
                  {isProcessing && (
                    <div className="w-4 h-4 border-2 border-border-strong border-t-accent rounded-full animate-spin-slow shrink-0" />
                  )}
                  {progress.message}
                </div>

                {/* Progress bar for analyzing step */}
                {progress.step === "analyzing" && progress.chunksTotal > 0 && (
                  <div className="space-y-1">
                    <div className="w-full bg-border rounded-full h-2 overflow-hidden">
                      <div
                        className="bg-accent h-2 rounded-full transition-all duration-500 ease-out"
                        style={{ width: `${progressPercent}%` }}
                      />
                    </div>
                    <p className="text-xs text-text-tertiary text-right">
                      {progress.chunksCompleted}/{progress.chunksTotal} 段 · {progressPercent}%
                    </p>
                  </div>
                )}
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
