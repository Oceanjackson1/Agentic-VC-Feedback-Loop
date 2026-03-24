"use client";

import { ScenarioMeta } from "@/lib/api";

const ICONS: Record<string, string> = {
  "chart-bar": "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
  "shopping-cart": "M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z",
  "user-check": "M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z",
  "clipboard-list": "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01",
};

interface Props {
  scenario: ScenarioMeta;
  onClick: (id: string) => void;
}

export function ScenarioCard({ scenario, onClick }: Props) {
  return (
    <button
      onClick={() => onClick(scenario.id)}
      className="group flex flex-col items-start p-6 rounded-2xl bg-card
                 hover:shadow-md transition-all duration-200 text-left cursor-pointer"
    >
      <div className="w-10 h-10 rounded-xl bg-accent-light flex items-center justify-center mb-4">
        <svg
          className="w-5 h-5 text-accent"
          fill="none"
          stroke="currentColor"
          strokeWidth={1.5}
          viewBox="0 0 24 24"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d={ICONS[scenario.icon] || ICONS["clipboard-list"]} />
        </svg>
      </div>
      <h3 className="text-base font-semibold text-text mb-1">{scenario.name_zh}</h3>
      <p className="text-sm text-text-secondary mb-3">{scenario.description_zh}</p>
      <span className="text-accent text-sm font-medium mt-auto group-hover:underline">
        开始分析 →
      </span>
    </button>
  );
}
