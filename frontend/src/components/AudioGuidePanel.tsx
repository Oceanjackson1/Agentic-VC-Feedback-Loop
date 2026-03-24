"use client";

import { useState, useEffect } from "react";

export function AudioGuidePanel() {
  const [collapsed, setCollapsed] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("audio_guide_collapsed");
    if (saved === "true") setCollapsed(true);
  }, []);

  const toggle = () => {
    const next = !collapsed;
    setCollapsed(next);
    localStorage.setItem("audio_guide_collapsed", String(next));
  };

  return (
    <div className="rounded-2xl bg-card overflow-hidden">
      {/* Header */}
      <button
        onClick={toggle}
        className="w-full flex items-center gap-3 px-5 py-4 text-left hover:bg-surface-hover transition-colors"
      >
        <div className="w-1 h-8 bg-accent rounded-full shrink-0" />
        <svg className="w-5 h-5 text-accent shrink-0" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
        <span className="text-sm font-medium text-text flex-1">有音频文件？免费转为文本后上传</span>
        <svg
          className={`w-4 h-4 text-text-tertiary transition-transform duration-200 ${collapsed ? "" : "rotate-180"}`}
          fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Content */}
      {!collapsed && (
        <div className="px-5 pb-5 space-y-4">
          <p className="text-sm text-text-secondary pl-9">
            本产品不直接支持音频格式。你可以通过以下免费工具将音频转为文本：
          </p>

          {/* Step 1 */}
          <div className="flex items-start gap-3 pl-9">
            <span className="text-accent text-sm font-semibold shrink-0 mt-0.5">01</span>
            <div className="flex-1">
              <p className="text-sm text-text mb-2">转录音频为文本</p>
              <a
                href="https://turboscribe.ai/zh-CN/dashboard"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-accent text-accent
                           text-sm font-medium hover:bg-accent-light transition-colors"
              >
                前往 TurboScribe（免费）
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
              <p className="text-xs text-text-tertiary mt-2">
                💡 注册多个邮箱可获取多次免费转录额度
              </p>
            </div>
          </div>

          {/* Step 2 */}
          <div className="flex items-start gap-3 pl-9">
            <span className="text-accent text-sm font-semibold shrink-0 mt-0.5">02</span>
            <div className="flex-1">
              <p className="text-sm text-text mb-2">音频太长？先裁剪</p>
              <a
                href="https://vocalremover.org/zh/cutter"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-border-strong text-text-secondary
                           text-sm font-medium hover:bg-bg-secondary transition-colors"
              >
                前往 Vocal Remover 裁剪
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          </div>

          <p className="text-xs text-text-tertiary pl-9">
            转录完成后，下载为 PDF、Word 或 TXT 格式，回到本页面上传即可。
          </p>
        </div>
      )}
    </div>
  );
}
