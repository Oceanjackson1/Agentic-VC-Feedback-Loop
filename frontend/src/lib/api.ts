const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://agentic-vc-feedback-loop-production.up.railway.app";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  return res;
}

async function handleError(res: Response): Promise<never> {
  const text = await res.text();
  let msg = text;
  try {
    const j = JSON.parse(text);
    msg = j.detail || j.message || text;
  } catch {}
  throw new Error(msg);
}

export interface ScenarioMeta {
  id: string;
  name_zh: string;
  name_en: string;
  description_zh: string;
  description_en: string;
  icon: string;
}

export async function fetchScenarios(): Promise<ScenarioMeta[]> {
  const res = await apiFetch("/api/scenarios");
  if (!res.ok) throw new Error("获取场景列表失败");
  return res.json();
}

// ── 分步分析 API ──

export interface ExtractResponse {
  chunks: string[];
  total_chunks: number;
  is_english_source: boolean;
  context_text: string | null;
  output_lang: string;
}

export interface ChunkResult {
  chunk_index: number;
  results: Record<string, unknown>[];
}

/** Step 1: 上传文件 → 提取文本 → 返回分段 */
export async function extractFile(
  file: File,
  scenario: string,
  language: string,
  contextFile?: File | null
): Promise<ExtractResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("scenario", scenario);
  form.append("language", language);
  if (contextFile) {
    form.append("context_file", contextFile);
  }
  const res = await apiFetch("/api/extract", { method: "POST", body: form });
  if (!res.ok) await handleError(res);
  return res.json();
}

/** Step 2: 分析单个文本块 */
export async function analyzeChunk(params: {
  chunk: string;
  chunk_index: number;
  total_chunks: number;
  scenario: string;
  output_lang: string;
  context_text: string | null;
}): Promise<ChunkResult> {
  const res = await apiFetch("/api/analyze-chunk", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) await handleError(res);
  return res.json();
}

/** Step 3: 翻译 + 导出 Excel */
export async function exportExcel(params: {
  results: Record<string, unknown>[];
  language: string;
  scenario: string;
  is_english_source: boolean;
  filename: string;
}): Promise<Blob> {
  const res = await apiFetch("/api/export", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) await handleError(res);
  return res.blob();
}

// ── 旧版一体化接口（保留兼容）──

export async function analyzeFile(
  file: File,
  scenario: string,
  language: string,
  contextFile?: File | null
): Promise<Blob> {
  const form = new FormData();
  form.append("file", file);
  form.append("scenario", scenario);
  form.append("language", language);
  if (contextFile) {
    form.append("context_file", contextFile);
  }
  const res = await apiFetch("/api/analyze", { method: "POST", body: form });
  if (!res.ok) await handleError(res);
  return res.blob();
}

export async function googleLogin(code: string, redirectUri: string) {
  const res = await fetch(`${API_BASE}/api/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code, redirect_uri: redirectUri }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "登录失败");
  }
  return res.json();
}
